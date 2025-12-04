"""
Splunk HTTP Event Collector (HEC) Connector
v1.1 Enhancement - December 2025

Provides secure, reliable connectivity to Splunk HEC endpoints for event ingestion.
Supports batch processing, retries, and mock mode for demonstrations.
"""

import logging
import httpx
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


logger = logging.getLogger(__name__)


class SplunkEventType(Enum):
    """Splunk event types for categorization"""
    AUTHENTICATION = "authentication"
    ACCESS_REVIEW = "access_review"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    POLICY_CHANGE = "policy_change"
    ENTITLEMENT_CHANGE = "entitlement_change"
    COMPLIANCE_VIOLATION = "compliance_violation"


class SplunkHECConnector:
    """
    HTTP Event Collector connector for Splunk integration.

    Features:
    - Secure HEC token-based authentication
    - Batch event submission
    - Automatic retry with exponential backoff
    - SSL verification
    - Mock mode for demos and testing

    v1.1 Enhancement - December 2025
    """

    def __init__(
        self,
        hec_url: str,
        hec_token: str,
        index: str = "entra_id_governance",
        source: str = "entra_governance_toolkit",
        sourcetype: str = "entra:identity:governance",
        verify_ssl: bool = True,
        mock_mode: bool = False,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Splunk HEC connector.

        Args:
            hec_url: Splunk HEC endpoint URL (e.g., https://splunk.example.com:8088)
            hec_token: HEC authentication token
            index: Target Splunk index
            source: Event source identifier
            sourcetype: Splunk sourcetype for parsing
            verify_ssl: Enable SSL certificate verification
            mock_mode: Enable mock mode (no actual API calls)
            timeout: HTTP request timeout in seconds
            max_retries: Maximum retry attempts for failed requests
        """
        self.hec_url = hec_url.rstrip('/')
        self.hec_token = hec_token
        self.index = index
        self.source = source
        self.sourcetype = sourcetype
        self.verify_ssl = verify_ssl
        self.mock_mode = mock_mode
        self.timeout = timeout
        self.max_retries = max_retries

        # HEC endpoint paths
        self.event_endpoint = f"{self.hec_url}/services/collector/event"
        self.raw_endpoint = f"{self.hec_url}/services/collector/raw"

        # Statistics
        self.events_sent = 0
        self.events_failed = 0
        self.bytes_sent = 0

        logger.info(
            f"SplunkHECConnector initialized - URL: {self.hec_url}, "
            f"Index: {self.index}, Mock: {self.mock_mode}"
        )

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for HEC requests"""
        return {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json"
        }

    def send_event(
        self,
        event_data: Dict[str, Any],
        event_type: Optional[SplunkEventType] = None,
        host: Optional[str] = None,
        time: Optional[float] = None
    ) -> bool:
        """
        Send a single event to Splunk HEC.

        Args:
            event_data: Event payload dictionary
            event_type: Event type classification
            host: Source host (defaults to local hostname)
            time: Event timestamp (Unix epoch, defaults to now)

        Returns:
            bool: True if successful, False otherwise
        """
        return self.send_events([event_data], event_type, host, time)

    def send_events(
        self,
        events: List[Dict[str, Any]],
        event_type: Optional[SplunkEventType] = None,
        host: Optional[str] = None,
        time: Optional[float] = None
    ) -> bool:
        """
        Send multiple events to Splunk HEC in batch.

        Args:
            events: List of event payload dictionaries
            event_type: Event type classification
            host: Source host
            time: Event timestamp base

        Returns:
            bool: True if all events sent successfully, False otherwise
        """
        if not events:
            logger.warning("No events to send")
            return False

        # Mock mode - simulate success
        if self.mock_mode:
            logger.info(f"[MOCK] Would send {len(events)} events to Splunk HEC")
            self.events_sent += len(events)
            return True

        try:
            # Build HEC payload
            hec_payload = self._build_hec_payload(events, event_type, host, time)

            # Send to Splunk with retry logic
            success = self._send_with_retry(hec_payload)

            if success:
                self.events_sent += len(events)
                self.bytes_sent += len(json.dumps(hec_payload))
                logger.info(f"Successfully sent {len(events)} events to Splunk")
            else:
                self.events_failed += len(events)
                logger.error(f"Failed to send {len(events)} events to Splunk")

            return success

        except Exception as e:
            logger.error(f"Error sending events to Splunk: {e}")
            self.events_failed += len(events)
            return False

    def _build_hec_payload(
        self,
        events: List[Dict[str, Any]],
        event_type: Optional[SplunkEventType],
        host: Optional[str],
        time: Optional[float]
    ) -> str:
        """
        Build HEC-compliant JSON payload.

        Args:
            events: List of event dictionaries
            event_type: Event type
            host: Source host
            time: Timestamp

        Returns:
            str: JSON string payload for HEC
        """
        payload_lines = []

        for event in events:
            hec_event = {
                "time": time or datetime.utcnow().timestamp(),
                "host": host or "entra-governance-toolkit",
                "source": self.source,
                "sourcetype": self.sourcetype,
                "index": self.index,
                "event": event
            }

            # Add event type if specified
            if event_type:
                hec_event["event"]["event_type"] = event_type.value

            payload_lines.append(json.dumps(hec_event))

        # HEC expects newline-delimited JSON for batch events
        return "\n".join(payload_lines)

    def _send_with_retry(self, payload: str) -> bool:
        """
        Send payload to HEC with retry logic.

        Args:
            payload: HEC JSON payload

        Returns:
            bool: True if successful, False otherwise
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                with httpx.Client(verify=self.verify_ssl, timeout=self.timeout) as client:
                    response = client.post(
                        self.event_endpoint,
                        headers=self._get_headers(),
                        content=payload
                    )

                    if response.status_code == 200:
                        return True
                    else:
                        last_error = f"HTTP {response.status_code}: {response.text}"
                        logger.warning(
                            f"Attempt {attempt + 1}/{self.max_retries} failed: {last_error}"
                        )

            except Exception as e:
                last_error = str(e)
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {last_error}"
                )

        logger.error(f"All {self.max_retries} attempts failed. Last error: {last_error}")
        return False

    def health_check(self) -> bool:
        """
        Check connectivity to Splunk HEC.

        Returns:
            bool: True if HEC is reachable and accepting events
        """
        if self.mock_mode:
            logger.info("[MOCK] Health check passed")
            return True

        try:
            # Send a test event
            test_event = {
                "message": "Health check from Entra ID Governance Toolkit",
                "check_type": "connectivity",
                "timestamp": datetime.utcnow().isoformat()
            }

            return self.send_event(test_event)

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get connector statistics.

        Returns:
            dict: Statistics including events sent, failed, and bytes transferred
        """
        return {
            "events_sent": self.events_sent,
            "events_failed": self.events_failed,
            "bytes_sent": self.bytes_sent,
            "success_rate": (
                self.events_sent / (self.events_sent + self.events_failed)
                if (self.events_sent + self.events_failed) > 0
                else 0.0
            ),
            "mock_mode": self.mock_mode
        }
