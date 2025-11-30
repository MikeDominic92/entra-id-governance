"""
Tests for Graph API Client
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.graph_client import GraphClient, GraphAPIError


class TestGraphClient:
    """Test suite for GraphClient"""

    @patch('src.graph_client.ConfidentialClientApplication')
    def test_client_initialization(self, mock_msal):
        """Test client initialization"""
        client = GraphClient()
        assert client.base_url == "https://graph.microsoft.com/v1.0"
        assert mock_msal.called

    @patch('src.graph_client.ConfidentialClientApplication')
    def test_beta_endpoint(self, mock_msal):
        """Test beta endpoint selection"""
        client = GraphClient(use_beta=True)
        assert client.base_url == "https://graph.microsoft.com/beta"

    @patch('src.graph_client.ConfidentialClientApplication')
    def test_token_acquisition(self, mock_msal):
        """Test access token acquisition"""
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test_token_123"
        }
        mock_app.get_accounts.return_value = []
        mock_msal.return_value = mock_app

        client = GraphClient()
        token = client.access_token

        assert token == "test_token_123"
        assert mock_app.acquire_token_for_client.called

    @patch('src.graph_client.ConfidentialClientApplication')
    def test_token_acquisition_failure(self, mock_msal):
        """Test token acquisition failure handling"""
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
            "error": "invalid_client",
            "error_description": "Invalid client secret"
        }
        mock_app.get_accounts.return_value = []
        mock_msal.return_value = mock_app

        client = GraphClient()

        with pytest.raises(GraphAPIError) as exc_info:
            _ = client.access_token

        assert "invalid_client" in str(exc_info.value)

    @patch('src.graph_client.httpx.Client')
    @patch('src.graph_client.ConfidentialClientApplication')
    def test_get_request_success(self, mock_msal, mock_httpx):
        """Test successful GET request"""
        # Setup MSAL mock
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test_token"
        }
        mock_app.get_accounts.return_value = []
        mock_msal.return_value = mock_app

        # Setup HTTP mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"value": []}'
        mock_response.json.return_value = {"value": []}

        mock_client_instance = MagicMock()
        mock_client_instance.__enter__.return_value.request.return_value = mock_response
        mock_httpx.return_value = mock_client_instance

        client = GraphClient()
        result = client.get("users")

        assert result == {"value": []}

    @patch('src.graph_client.ConfidentialClientApplication')
    def test_pagination(self, mock_msal):
        """Test pagination handling"""
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test_token"
        }
        mock_app.get_accounts.return_value = []
        mock_msal.return_value = mock_app

        client = GraphClient()

        # Mock paginated responses
        with patch.object(client, 'get') as mock_get:
            mock_get.side_effect = [
                {
                    "value": [{"id": "1"}, {"id": "2"}],
                    "@odata.nextLink": "https://graph.microsoft.com/v1.0/users?$skip=2"
                },
                {
                    "value": [{"id": "3"}]
                }
            ]

            results = client.get_all_pages("users")

            assert len(results) == 3
            assert results[0]["id"] == "1"
            assert results[2]["id"] == "3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
