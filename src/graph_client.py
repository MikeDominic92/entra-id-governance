"""
Microsoft Graph API Client with authentication and error handling
"""

import json
import time
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import httpx
from msal import ConfidentialClientApplication, SerializableTokenCache

from .config import settings

logger = logging.getLogger(__name__)


class GraphAPIError(Exception):
    """Custom exception for Graph API errors"""
    pass


class GraphClient:
    """
    Microsoft Graph API client with authentication, caching, and retry logic
    """

    GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"
    GRAPH_BETA_ENDPOINT = "https://graph.microsoft.com/beta"

    def __init__(self, use_beta: bool = False):
        """
        Initialize Graph API client

        Args:
            use_beta: Use beta endpoint instead of v1.0
        """
        self.config = settings.graph
        self.app_config = settings.app
        self.base_url = self.GRAPH_BETA_ENDPOINT if use_beta else self.GRAPH_ENDPOINT
        self.token_cache = self._load_token_cache()
        self.msal_app = self._create_msal_app()
        self._access_token: Optional[str] = None

    def _load_token_cache(self) -> SerializableTokenCache:
        """Load token cache from file"""
        cache = SerializableTokenCache()
        cache_file = Path(self.app_config.token_cache_file)

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cache.deserialize(f.read())
                logger.info("Token cache loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load token cache: {e}")

        return cache

    def _save_token_cache(self):
        """Save token cache to file"""
        if self.token_cache.has_state_changed:
            try:
                cache_file = Path(self.app_config.token_cache_file)
                with open(cache_file, 'w') as f:
                    f.write(self.token_cache.serialize())
                logger.debug("Token cache saved")
            except Exception as e:
                logger.warning(f"Failed to save token cache: {e}")

    def _create_msal_app(self) -> ConfidentialClientApplication:
        """Create MSAL confidential client application"""
        return ConfidentialClientApplication(
            client_id=self.config.client_id,
            client_credential=self.config.client_secret,
            authority=self.config.authority_url,
            token_cache=self.token_cache
        )

    def _acquire_token(self) -> str:
        """
        Acquire access token using client credentials flow

        Returns:
            Access token string

        Raises:
            GraphAPIError: If token acquisition fails
        """
        # Try to get token from cache
        accounts = self.msal_app.get_accounts()
        result = None

        if accounts:
            result = self.msal_app.acquire_token_silent(
                scopes=self.config.scopes,
                account=accounts[0]
            )

        # If no cached token, acquire new one
        if not result:
            logger.info("Acquiring new access token")
            result = self.msal_app.acquire_token_for_client(
                scopes=self.config.scopes
            )

        self._save_token_cache()

        if "access_token" in result:
            logger.info("Access token acquired successfully")
            return result["access_token"]
        else:
            error = result.get("error", "Unknown error")
            error_desc = result.get("error_description", "No description")
            raise GraphAPIError(f"Token acquisition failed: {error} - {error_desc}")

    @property
    def access_token(self) -> str:
        """Get current access token, acquiring if necessary"""
        if not self._access_token:
            self._access_token = self._acquire_token()
        return self._access_token

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Graph API with retry logic

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST/PATCH
            retry_count: Current retry attempt

        Returns:
            Response JSON

        Raises:
            GraphAPIError: If request fails after retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_data
                )

                # Handle rate limiting (429)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", self.app_config.retry_delay))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    return self._make_request(method, endpoint, params, json_data, retry_count)

                # Handle token expiration (401)
                if response.status_code == 401:
                    logger.info("Token expired, acquiring new token")
                    self._access_token = None
                    if retry_count < self.app_config.max_retries:
                        return self._make_request(method, endpoint, params, json_data, retry_count + 1)

                # Raise for other HTTP errors
                response.raise_for_status()

                return response.json() if response.content else {}

        except httpx.HTTPStatusError as e:
            if retry_count < self.app_config.max_retries:
                wait_time = self.app_config.retry_delay * (2 ** retry_count)
                logger.warning(f"Request failed, retrying in {wait_time}s... (attempt {retry_count + 1})")
                time.sleep(wait_time)
                return self._make_request(method, endpoint, params, json_data, retry_count + 1)
            else:
                error_detail = e.response.text
                raise GraphAPIError(f"HTTP {e.response.status_code}: {error_detail}")

        except Exception as e:
            raise GraphAPIError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request("POST", endpoint, json_data=json_data)

    def patch(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PATCH request"""
        return self._make_request("PATCH", endpoint, json_data=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint)

    def get_all_pages(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Get all pages of results using pagination

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            List of all items across all pages
        """
        all_items = []
        next_link = None
        first_request = True

        while first_request or next_link:
            if first_request:
                response = self.get(endpoint, params)
                first_request = False
            else:
                # Extract relative path from next link
                next_url = next_link.replace(self.base_url, "")
                response = self.get(next_url)

            # Handle different response formats
            if "value" in response:
                all_items.extend(response["value"])
                next_link = response.get("@odata.nextLink")
            else:
                all_items.append(response)
                break

            if not next_link:
                break

        logger.info(f"Retrieved {len(all_items)} items from {endpoint}")
        return all_items

    def batch_request(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute batch requests (up to 20 at a time)

        Args:
            requests: List of request objects with 'id', 'method', 'url' keys

        Returns:
            List of response objects
        """
        if len(requests) > 20:
            logger.warning(f"Batch size {len(requests)} exceeds limit. Splitting into chunks.")
            results = []
            for i in range(0, len(requests), 20):
                chunk = requests[i:i + 20]
                results.extend(self.batch_request(chunk))
            return results

        batch_body = {"requests": requests}
        response = self.post("$batch", batch_body)

        return response.get("responses", [])
