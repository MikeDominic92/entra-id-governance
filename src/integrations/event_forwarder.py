"""
Event Forwarder for Entra ID Governance Events to Splunk
v1.1 Enhancement - December 2025

Forwards identity governance events to Splunk in CIM-compliant format.
Supports access reviews, entitlement changes, PIM activations, and policy changes.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from .splunk_connector import SplunkHECConnector, SplunkEventType


logger = logging.getLogger(__name__)


class CIMDataModel(Enum):
    """Splunk Common Information Model data models"""
    AUTHENTICATION = "Authentication"
    CHANGE = "Change"
    IDENTITY_MANAGEMENT = "Identity_Management"
    ACCESS = "Access"
    RISK = "Risk"


class EventForwarder:
    """
    Forward Entra ID governance events to Splunk in CIM format.

    Maps Entra ID events to Splunk Common Information Model (CIM) for:
    - Identity Management data model
    - Change data model
    - Authentication data model
    - Access data model

    v1.1 Enhancement - December 2025
    """

    def __init__(self, splunk_connector: SplunkHECConnector):
        """
        Initialize event forwarder.

        Args:
            splunk_connector: Configured SplunkHECConnector instance
        """
        self.connector = splunk_connector
        self.events_forwarded = 0

        logger.info("EventForwarder initialized")

    def forward_access_review_event(
        self,
        review_id: str,
        review_name: str,
        status: str,
        target_resource: str,
        reviewer: str,
        decision: Optional[str] = None,
        justification: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Forward access review event to Splunk.

        Args:
            review_id: Unique review identifier
            review_name: Review display name
            status: Review status (pending, approved, denied, completed)
            target_resource: Resource being reviewed
            reviewer: User performing review
            decision: Review decision
            justification: Decision justification
            metadata: Additional metadata

        Returns:
            bool: True if forwarded successfully
        """
        # Map to CIM Identity Management data model
        cim_event = {
            # CIM fields
            "datamodel": CIMDataModel.IDENTITY_MANAGEMENT.value,
            "action": "access_review",
            "status": status,
            "user": reviewer,
            "object": target_resource,
            "result": decision or "pending",

            # Entra ID specific fields
            "review_id": review_id,
            "review_name": review_name,
            "justification": justification,

            # Metadata
            "vendor": "Microsoft",
            "product": "Entra ID",
            "category": "Identity Governance",
            "severity": self._calculate_review_severity(status, decision),
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add additional metadata
        if metadata:
            cim_event.update(metadata)

        success = self.connector.send_event(
            cim_event,
            event_type=SplunkEventType.ACCESS_REVIEW
        )

        if success:
            self.events_forwarded += 1

        return success

    def forward_pim_activation_event(
        self,
        activation_id: str,
        role_name: str,
        user_principal_name: str,
        activation_duration: int,
        justification: str,
        status: str,
        risk_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Forward PIM role activation event to Splunk.

        Args:
            activation_id: Unique activation identifier
            role_name: Role being activated
            user_principal_name: User requesting activation
            activation_duration: Duration in minutes
            justification: Activation justification
            status: Activation status (requested, approved, denied, active)
            risk_score: Calculated risk score (0-100)
            metadata: Additional metadata

        Returns:
            bool: True if forwarded successfully
        """
        # Map to CIM Identity Management data model
        cim_event = {
            # CIM fields
            "datamodel": CIMDataModel.IDENTITY_MANAGEMENT.value,
            "action": "privilege_escalation",
            "status": status,
            "user": user_principal_name,
            "object": role_name,
            "result": status,

            # Entra ID specific fields
            "activation_id": activation_id,
            "activation_duration_minutes": activation_duration,
            "justification": justification,
            "risk_score": risk_score or 0.0,

            # Metadata
            "vendor": "Microsoft",
            "product": "Entra ID PIM",
            "category": "Privileged Access",
            "severity": self._calculate_pim_severity(role_name, risk_score),
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add additional metadata
        if metadata:
            cim_event.update(metadata)

        success = self.connector.send_event(
            cim_event,
            event_type=SplunkEventType.PRIVILEGE_ESCALATION
        )

        if success:
            self.events_forwarded += 1

        return success

    def forward_policy_change_event(
        self,
        policy_id: str,
        policy_name: str,
        policy_type: str,
        change_type: str,
        changed_by: str,
        changes: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Forward Conditional Access policy change event to Splunk.

        Args:
            policy_id: Policy identifier
            policy_name: Policy display name
            policy_type: Type of policy (ConditionalAccess, etc.)
            change_type: Type of change (created, modified, deleted, enabled, disabled)
            changed_by: User who made the change
            changes: Dictionary of field changes
            metadata: Additional metadata

        Returns:
            bool: True if forwarded successfully
        """
        # Map to CIM Change data model
        cim_event = {
            # CIM fields
            "datamodel": CIMDataModel.CHANGE.value,
            "action": change_type,
            "status": "success",
            "user": changed_by,
            "object": policy_name,
            "object_category": policy_type,
            "result": "success",

            # Entra ID specific fields
            "policy_id": policy_id,
            "changes": changes,

            # Metadata
            "vendor": "Microsoft",
            "product": "Entra ID",
            "category": "Policy Management",
            "severity": self._calculate_policy_change_severity(change_type, policy_type),
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add additional metadata
        if metadata:
            cim_event.update(metadata)

        success = self.connector.send_event(
            cim_event,
            event_type=SplunkEventType.POLICY_CHANGE
        )

        if success:
            self.events_forwarded += 1

        return success

    def forward_entitlement_change_event(
        self,
        entitlement_id: str,
        entitlement_name: str,
        change_type: str,
        affected_user: str,
        resource: str,
        access_level: str,
        changed_by: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Forward entitlement management change event to Splunk.

        Args:
            entitlement_id: Entitlement identifier
            entitlement_name: Entitlement display name
            change_type: Type of change (granted, revoked, modified)
            affected_user: User affected by change
            resource: Resource being accessed
            access_level: Level of access granted
            changed_by: User who made the change
            metadata: Additional metadata

        Returns:
            bool: True if forwarded successfully
        """
        # Map to CIM Identity Management data model
        cim_event = {
            # CIM fields
            "datamodel": CIMDataModel.IDENTITY_MANAGEMENT.value,
            "action": change_type,
            "status": "success",
            "user": affected_user,
            "object": resource,
            "result": "success",

            # Entra ID specific fields
            "entitlement_id": entitlement_id,
            "entitlement_name": entitlement_name,
            "access_level": access_level,
            "changed_by": changed_by,

            # Metadata
            "vendor": "Microsoft",
            "product": "Entra ID",
            "category": "Entitlement Management",
            "severity": self._calculate_entitlement_severity(change_type, access_level),
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add additional metadata
        if metadata:
            cim_event.update(metadata)

        success = self.connector.send_event(
            cim_event,
            event_type=SplunkEventType.ENTITLEMENT_CHANGE
        )

        if success:
            self.events_forwarded += 1

        return success

    def forward_compliance_violation_event(
        self,
        violation_id: str,
        violation_type: str,
        severity: str,
        affected_entity: str,
        description: str,
        remediation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Forward compliance violation event to Splunk.

        Args:
            violation_id: Violation identifier
            violation_type: Type of violation
            severity: Severity level (critical, high, medium, low, info)
            affected_entity: Entity in violation
            description: Violation description
            remediation: Recommended remediation
            metadata: Additional metadata

        Returns:
            bool: True if forwarded successfully
        """
        # Map to CIM Risk data model
        cim_event = {
            # CIM fields
            "datamodel": CIMDataModel.RISK.value,
            "action": "violation_detected",
            "status": "detected",
            "object": affected_entity,
            "result": violation_type,

            # Entra ID specific fields
            "violation_id": violation_id,
            "violation_type": violation_type,
            "description": description,
            "remediation": remediation,

            # Metadata
            "vendor": "Microsoft",
            "product": "Entra ID Governance",
            "category": "Compliance",
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add additional metadata
        if metadata:
            cim_event.update(metadata)

        success = self.connector.send_event(
            cim_event,
            event_type=SplunkEventType.COMPLIANCE_VIOLATION
        )

        if success:
            self.events_forwarded += 1

        return success

    def forward_batch_events(
        self,
        events: List[Dict[str, Any]],
        event_type: SplunkEventType
    ) -> bool:
        """
        Forward multiple events in batch.

        Args:
            events: List of event dictionaries
            event_type: Type of events

        Returns:
            bool: True if all events forwarded successfully
        """
        success = self.connector.send_events(events, event_type)

        if success:
            self.events_forwarded += len(events)

        return success

    def _calculate_review_severity(
        self,
        status: str,
        decision: Optional[str]
    ) -> str:
        """Calculate severity for access review events"""
        if decision == "denied":
            return "medium"
        elif status == "overdue":
            return "high"
        elif status == "completed":
            return "low"
        return "info"

    def _calculate_pim_severity(
        self,
        role_name: str,
        risk_score: Optional[float]
    ) -> str:
        """Calculate severity for PIM activation events"""
        high_risk_roles = [
            "Global Administrator",
            "Privileged Role Administrator",
            "Security Administrator"
        ]

        if role_name in high_risk_roles:
            return "high"
        elif risk_score and risk_score > 70:
            return "high"
        elif risk_score and risk_score > 40:
            return "medium"
        return "low"

    def _calculate_policy_change_severity(
        self,
        change_type: str,
        policy_type: str
    ) -> str:
        """Calculate severity for policy change events"""
        if change_type in ["deleted", "disabled"]:
            return "high"
        elif change_type == "created":
            return "medium"
        elif change_type == "modified":
            return "medium"
        return "low"

    def _calculate_entitlement_severity(
        self,
        change_type: str,
        access_level: str
    ) -> str:
        """Calculate severity for entitlement change events"""
        if change_type == "granted" and "admin" in access_level.lower():
            return "high"
        elif change_type == "revoked":
            return "low"
        return "medium"

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get forwarder statistics.

        Returns:
            dict: Statistics including events forwarded and connector stats
        """
        return {
            "events_forwarded": self.events_forwarded,
            "connector_stats": self.connector.get_statistics()
        }
