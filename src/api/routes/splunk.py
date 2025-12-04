"""
Splunk SIEM Integration API Routes
v1.1 Enhancement - December 2025

REST API endpoints for Splunk integration management and webhook reception.
"""

import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from pydantic import BaseModel, Field

from ...config import settings
from ...integrations import SplunkHECConnector, EventForwarder, AlertReceiver
from ...integrations.alert_receiver import SplunkAlert, AlertSeverity, AlertCategory


logger = logging.getLogger(__name__)
router = APIRouter()

# Global instances (initialized on first use)
_connector: Optional[SplunkHECConnector] = None
_forwarder: Optional[EventForwarder] = None
_receiver: Optional[AlertReceiver] = None


def get_connector() -> SplunkHECConnector:
    """Get or create Splunk connector instance"""
    global _connector
    if _connector is None:
        config = settings.splunk
        _connector = SplunkHECConnector(
            hec_url=config.hec_url,
            hec_token=config.hec_token,
            index=config.index,
            source=config.source,
            sourcetype=config.sourcetype,
            verify_ssl=config.verify_ssl,
            mock_mode=config.mock_mode,
            timeout=config.timeout,
            max_retries=config.max_retries,
        )
    return _connector


def get_forwarder() -> EventForwarder:
    """Get or create event forwarder instance"""
    global _forwarder
    if _forwarder is None:
        _forwarder = EventForwarder(get_connector())
    return _forwarder


def get_receiver() -> AlertReceiver:
    """Get or create alert receiver instance"""
    global _receiver
    if _receiver is None:
        config = settings.splunk
        _receiver = AlertReceiver(enable_auto_remediation=config.auto_remediation)
    return _receiver


# Request/Response Models
class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    enabled: bool
    mock_mode: bool
    hec_reachable: bool
    configuration_valid: bool


class StatisticsResponse(BaseModel):
    """Statistics response model"""
    connector: Dict[str, Any]
    forwarder: Dict[str, Any]
    receiver: Dict[str, Any]


class ForwardEventRequest(BaseModel):
    """Manual event forwarding request"""
    event_type: str = Field(..., description="Event type (access_review, pim_activation, etc.)")
    event_data: Dict[str, Any] = Field(..., description="Event payload")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class AlertWebhookPayload(BaseModel):
    """Splunk alert webhook payload"""
    alert_id: str
    search_name: str
    severity: str
    category: str
    description: str
    affected_user: Optional[str] = None
    affected_resource: Optional[str] = None
    source_ip: Optional[str] = None
    event_count: int = 1
    time_window: int = 300
    correlation_score: float = 0.0
    first_seen: str
    last_seen: str
    raw_events: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


# API Endpoints

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Check Splunk integration health status.

    v1.1 Enhancement - December 2025
    """
    try:
        config = settings.splunk
        connector = get_connector()

        # Test HEC connectivity
        hec_reachable = connector.health_check() if config.enabled else False

        return HealthCheckResponse(
            status="healthy" if (config.enabled and hec_reachable) or config.mock_mode else "disabled",
            enabled=config.enabled,
            mock_mode=config.mock_mode,
            hec_reachable=hec_reachable,
            configuration_valid=True,
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_configuration():
    """
    Get current Splunk integration configuration (sanitized).

    v1.1 Enhancement - December 2025
    """
    try:
        config = settings.splunk

        return {
            "enabled": config.enabled,
            "mock_mode": config.mock_mode,
            "hec_url": config.hec_url,
            "index": config.index,
            "source": config.source,
            "sourcetype": config.sourcetype,
            "verify_ssl": config.verify_ssl,
            "timeout": config.timeout,
            "max_retries": config.max_retries,
            "auto_remediation": config.auto_remediation,
            "event_forwarding": {
                "access_reviews": config.forward_access_reviews,
                "pim_activations": config.forward_pim_activations,
                "policy_changes": config.forward_policy_changes,
                "compliance_violations": config.forward_compliance_violations,
            },
        }

    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    Get Splunk integration statistics.

    v1.1 Enhancement - December 2025
    """
    try:
        connector = get_connector()
        forwarder = get_forwarder()
        receiver = get_receiver()

        return StatisticsResponse(
            connector=connector.get_statistics(),
            forwarder=forwarder.get_statistics(),
            receiver=receiver.get_statistics(),
        )

    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/events/forward")
async def forward_event(request: ForwardEventRequest, background_tasks: BackgroundTasks):
    """
    Manually forward an event to Splunk.

    v1.1 Enhancement - December 2025
    """
    try:
        config = settings.splunk

        if not config.enabled and not config.mock_mode:
            raise HTTPException(
                status_code=400,
                detail="Splunk integration is not enabled"
            )

        forwarder = get_forwarder()

        # Forward based on event type
        if request.event_type == "access_review":
            success = forwarder.forward_access_review_event(
                review_id=request.event_data.get("review_id", ""),
                review_name=request.event_data.get("review_name", ""),
                status=request.event_data.get("status", ""),
                target_resource=request.event_data.get("target_resource", ""),
                reviewer=request.event_data.get("reviewer", ""),
                decision=request.event_data.get("decision"),
                justification=request.event_data.get("justification"),
                metadata=request.metadata,
            )
        elif request.event_type == "pim_activation":
            success = forwarder.forward_pim_activation_event(
                activation_id=request.event_data.get("activation_id", ""),
                role_name=request.event_data.get("role_name", ""),
                user_principal_name=request.event_data.get("user_principal_name", ""),
                activation_duration=request.event_data.get("activation_duration", 60),
                justification=request.event_data.get("justification", ""),
                status=request.event_data.get("status", ""),
                risk_score=request.event_data.get("risk_score"),
                metadata=request.metadata,
            )
        elif request.event_type == "policy_change":
            success = forwarder.forward_policy_change_event(
                policy_id=request.event_data.get("policy_id", ""),
                policy_name=request.event_data.get("policy_name", ""),
                policy_type=request.event_data.get("policy_type", ""),
                change_type=request.event_data.get("change_type", ""),
                changed_by=request.event_data.get("changed_by", ""),
                changes=request.event_data.get("changes", {}),
                metadata=request.metadata,
            )
        elif request.event_type == "compliance_violation":
            success = forwarder.forward_compliance_violation_event(
                violation_id=request.event_data.get("violation_id", ""),
                violation_type=request.event_data.get("violation_type", ""),
                severity=request.event_data.get("severity", ""),
                affected_entity=request.event_data.get("affected_entity", ""),
                description=request.event_data.get("description", ""),
                remediation=request.event_data.get("remediation"),
                metadata=request.metadata,
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown event type: {request.event_type}"
            )

        if success:
            return {
                "status": "success",
                "message": "Event forwarded to Splunk",
                "event_type": request.event_type,
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to forward event to Splunk"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error forwarding event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/webhook")
async def receive_alert(payload: AlertWebhookPayload, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for receiving Splunk correlation alerts.

    This endpoint should be configured as the webhook destination in Splunk alerts.

    v1.1 Enhancement - December 2025
    """
    try:
        receiver = get_receiver()

        # Process alert in background
        result = receiver.receive_alert(payload.dict())

        return {
            "status": "received",
            "alert_id": payload.alert_id,
            "processing_result": result,
        }

    except Exception as e:
        logger.error(f"Error receiving alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/history")
async def get_alert_history(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 100,
):
    """
    Get alert reception history.

    v1.1 Enhancement - December 2025
    """
    try:
        receiver = get_receiver()

        # Convert string parameters to enums if provided
        category_enum = None
        if category:
            try:
                category_enum = AlertCategory(category)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category: {category}"
                )

        severity_enum = None
        if severity:
            try:
                severity_enum = AlertSeverity(severity)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid severity: {severity}"
                )

        history = receiver.get_alert_history(
            category=category_enum,
            severity=severity_enum,
            limit=limit,
        )

        return {
            "count": len(history),
            "alerts": history,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting alert history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/send-event")
async def test_send_event():
    """
    Send a test event to Splunk for connectivity testing.

    v1.1 Enhancement - December 2025
    """
    try:
        config = settings.splunk

        if not config.enabled and not config.mock_mode:
            raise HTTPException(
                status_code=400,
                detail="Splunk integration is not enabled"
            )

        connector = get_connector()

        test_event = {
            "message": "Test event from Entra ID Governance Toolkit",
            "test_type": "api_test",
            "source": "splunk_api_route",
            "version": "1.1.0",
        }

        success = connector.send_event(test_event)

        if success:
            return {
                "status": "success",
                "message": "Test event sent successfully",
                "mock_mode": config.mock_mode,
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to send test event"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending test event: {e}")
        raise HTTPException(status_code=500, detail=str(e))
