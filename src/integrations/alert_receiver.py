"""
Alert Receiver for Splunk Correlation Alerts
v1.1 Enhancement - December 2025

Receives and processes correlation alerts from Splunk via webhook.
Calculates correlation scores and triggers automated remediation workflows.
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertCategory(Enum):
    """Alert categories for correlation"""
    ANOMALOUS_ACCESS = "anomalous_access"
    PRIVILEGE_ABUSE = "privilege_abuse"
    POLICY_VIOLATION = "policy_violation"
    SUSPICIOUS_AUTHENTICATION = "suspicious_authentication"
    COMPLIANCE_RISK = "compliance_risk"
    LATERAL_MOVEMENT = "lateral_movement"


class SplunkAlert(BaseModel):
    """
    Splunk alert payload model.

    v1.1 Enhancement - December 2025
    """
    alert_id: str = Field(..., description="Unique alert identifier")
    search_name: str = Field(..., description="Name of Splunk search that triggered alert")
    severity: AlertSeverity = Field(..., description="Alert severity")
    category: AlertCategory = Field(..., description="Alert category")
    description: str = Field(..., description="Alert description")

    # Affected entities
    affected_user: Optional[str] = Field(None, description="User involved in alert")
    affected_resource: Optional[str] = Field(None, description="Resource involved in alert")
    source_ip: Optional[str] = Field(None, description="Source IP address")

    # Correlation data
    event_count: int = Field(default=1, description="Number of correlated events")
    time_window: int = Field(default=300, description="Time window in seconds")
    correlation_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Correlation score")

    # Timestamps
    first_seen: str = Field(..., description="First event timestamp")
    last_seen: str = Field(..., description="Last event timestamp")
    triggered_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    # Additional context
    raw_events: Optional[List[Dict[str, Any]]] = Field(None, description="Raw correlated events")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @validator("correlation_score")
    def validate_score(cls, v):
        """Validate correlation score is within valid range"""
        if not 0 <= v <= 100:
            raise ValueError("Correlation score must be between 0 and 100")
        return v


class AlertReceiver:
    """
    Receive and process Splunk correlation alerts.

    Features:
    - Webhook endpoint for Splunk alerts
    - Alert validation and parsing
    - Correlation score calculation
    - Automated remediation workflow triggering
    - Alert deduplication
    - Statistics tracking

    v1.1 Enhancement - December 2025
    """

    def __init__(self, enable_auto_remediation: bool = False):
        """
        Initialize alert receiver.

        Args:
            enable_auto_remediation: Enable automatic remediation workflows
        """
        self.enable_auto_remediation = enable_auto_remediation
        self.alerts_received = 0
        self.alerts_processed = 0
        self.alerts_failed = 0
        self.remediation_actions_taken = 0

        # Alert deduplication cache (alert_id -> timestamp)
        self._alert_cache: Dict[str, datetime] = {}
        self._cache_ttl = 3600  # 1 hour

        # Remediation handlers
        self._remediation_handlers: Dict[AlertCategory, List[Callable]] = {
            category: [] for category in AlertCategory
        }

        logger.info(
            f"AlertReceiver initialized - Auto-remediation: {enable_auto_remediation}"
        )

    def register_remediation_handler(
        self,
        category: AlertCategory,
        handler: Callable[[SplunkAlert], bool]
    ) -> None:
        """
        Register a remediation handler for an alert category.

        Args:
            category: Alert category
            handler: Callable that takes SplunkAlert and returns success bool
        """
        if category not in self._remediation_handlers:
            self._remediation_handlers[category] = []

        self._remediation_handlers[category].append(handler)
        logger.info(f"Registered remediation handler for {category.value}")

    def receive_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receive and process an alert from Splunk.

        Args:
            alert_data: Alert payload from Splunk webhook

        Returns:
            dict: Processing result with status and actions taken
        """
        self.alerts_received += 1

        try:
            # Parse and validate alert
            alert = SplunkAlert(**alert_data)

            # Check for duplicate
            if self._is_duplicate(alert):
                logger.info(f"Duplicate alert detected: {alert.alert_id}")
                return {
                    "status": "duplicate",
                    "alert_id": alert.alert_id,
                    "message": "Alert already processed"
                }

            # Calculate enhanced correlation score
            enhanced_score = self._calculate_correlation_score(alert)
            alert.correlation_score = enhanced_score

            # Process the alert
            result = self._process_alert(alert)

            self.alerts_processed += 1

            # Cache alert to prevent duplicates
            self._cache_alert(alert)

            return result

        except Exception as e:
            logger.error(f"Error processing alert: {e}")
            self.alerts_failed += 1
            return {
                "status": "error",
                "message": str(e)
            }

    def _process_alert(self, alert: SplunkAlert) -> Dict[str, Any]:
        """
        Process a validated alert.

        Args:
            alert: Validated SplunkAlert

        Returns:
            dict: Processing result
        """
        logger.info(
            f"Processing alert: {alert.alert_id} | "
            f"Severity: {alert.severity.value} | "
            f"Category: {alert.category.value} | "
            f"Score: {alert.correlation_score}"
        )

        result = {
            "status": "processed",
            "alert_id": alert.alert_id,
            "severity": alert.severity.value,
            "category": alert.category.value,
            "correlation_score": alert.correlation_score,
            "actions_taken": []
        }

        # Trigger remediation if enabled and score is high enough
        if self.enable_auto_remediation and alert.correlation_score >= 70:
            remediation_result = self._trigger_remediation(alert)
            result["actions_taken"] = remediation_result
            self.remediation_actions_taken += len(remediation_result)

        return result

    def _calculate_correlation_score(self, alert: SplunkAlert) -> float:
        """
        Calculate enhanced correlation score based on multiple factors.

        Factors considered:
        - Base Splunk correlation score
        - Alert severity
        - Event frequency
        - Time window
        - Affected entity criticality

        Args:
            alert: SplunkAlert to score

        Returns:
            float: Enhanced correlation score (0-100)
        """
        # Start with base score
        score = alert.correlation_score

        # Adjust for severity
        severity_weights = {
            AlertSeverity.CRITICAL: 1.3,
            AlertSeverity.HIGH: 1.2,
            AlertSeverity.MEDIUM: 1.0,
            AlertSeverity.LOW: 0.8,
            AlertSeverity.INFO: 0.5
        }
        score *= severity_weights.get(alert.severity, 1.0)

        # Adjust for event frequency
        if alert.event_count > 10:
            score *= 1.2
        elif alert.event_count > 5:
            score *= 1.1

        # Adjust for time window (shorter = more suspicious)
        if alert.time_window < 60:  # Less than 1 minute
            score *= 1.3
        elif alert.time_window < 300:  # Less than 5 minutes
            score *= 1.1

        # Adjust for privileged users
        if alert.affected_user and any(
            keyword in alert.affected_user.lower()
            for keyword in ["admin", "privileged", "global"]
        ):
            score *= 1.2

        # Cap at 100
        return min(score, 100.0)

    def _trigger_remediation(self, alert: SplunkAlert) -> List[str]:
        """
        Trigger automated remediation workflows.

        Args:
            alert: Alert to remediate

        Returns:
            list: List of actions taken
        """
        actions_taken = []

        # Get handlers for this category
        handlers = self._remediation_handlers.get(alert.category, [])

        if not handlers:
            logger.warning(
                f"No remediation handlers registered for {alert.category.value}"
            )
            return actions_taken

        # Execute each handler
        for handler in handlers:
            try:
                success = handler(alert)
                if success:
                    action_name = handler.__name__
                    actions_taken.append(action_name)
                    logger.info(
                        f"Remediation action '{action_name}' completed successfully"
                    )
            except Exception as e:
                logger.error(f"Remediation handler failed: {e}")

        return actions_taken

    def _is_duplicate(self, alert: SplunkAlert) -> bool:
        """
        Check if alert is a duplicate within cache TTL.

        Args:
            alert: Alert to check

        Returns:
            bool: True if duplicate, False otherwise
        """
        if alert.alert_id in self._alert_cache:
            cached_time = self._alert_cache[alert.alert_id]
            age = (datetime.utcnow() - cached_time).total_seconds()

            if age < self._cache_ttl:
                return True
            else:
                # Expired, remove from cache
                del self._alert_cache[alert.alert_id]

        return False

    def _cache_alert(self, alert: SplunkAlert) -> None:
        """
        Add alert to deduplication cache.

        Args:
            alert: Alert to cache
        """
        self._alert_cache[alert.alert_id] = datetime.utcnow()

        # Clean up old entries
        self._cleanup_cache()

    def _cleanup_cache(self) -> None:
        """Remove expired entries from alert cache"""
        now = datetime.utcnow()
        expired_ids = [
            alert_id for alert_id, timestamp in self._alert_cache.items()
            if (now - timestamp).total_seconds() > self._cache_ttl
        ]

        for alert_id in expired_ids:
            del self._alert_cache[alert_id]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get receiver statistics.

        Returns:
            dict: Statistics including alerts received, processed, and actions taken
        """
        return {
            "alerts_received": self.alerts_received,
            "alerts_processed": self.alerts_processed,
            "alerts_failed": self.alerts_failed,
            "success_rate": (
                self.alerts_processed / self.alerts_received
                if self.alerts_received > 0
                else 0.0
            ),
            "remediation_actions_taken": self.remediation_actions_taken,
            "auto_remediation_enabled": self.enable_auto_remediation,
            "cached_alerts": len(self._alert_cache)
        }

    def get_alert_history(
        self,
        category: Optional[AlertCategory] = None,
        severity: Optional[AlertSeverity] = None,
        limit: int = 100
    ) -> List[str]:
        """
        Get cached alert IDs matching criteria.

        Args:
            category: Filter by category
            severity: Filter by severity
            limit: Maximum results to return

        Returns:
            list: Alert IDs matching criteria
        """
        # In production, this would query a persistent store
        # For now, return cached alert IDs
        return list(self._alert_cache.keys())[:limit]
