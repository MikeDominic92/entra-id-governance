"""
PIM (Privileged Identity Management) API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from ...analyzers import PIMAnalyzer
from ...automation import PIMActivator

router = APIRouter()


class ActivateRoleRequest(BaseModel):
    """Request model for role activation"""
    principal_id: str
    role_definition_id: str
    justification: str
    duration_hours: int = 8
    ticket_number: Optional[str] = None


class DeactivateRoleRequest(BaseModel):
    """Request model for role deactivation"""
    principal_id: str
    role_definition_id: str
    justification: str = "Manual deactivation"


@router.get("/roles/definitions")
async def get_role_definitions():
    """Get all directory role definitions"""
    try:
        analyzer = PIMAnalyzer()
        roles = analyzer.get_role_definitions()
        return {"count": len(roles), "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assignments/eligible")
async def get_eligible_assignments():
    """Get all eligible (PIM) role assignments"""
    try:
        analyzer = PIMAnalyzer()
        assignments = analyzer.get_eligible_assignments()
        return {"count": len(assignments), "assignments": assignments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assignments/active")
async def get_active_assignments():
    """Get all active role assignments"""
    try:
        analyzer = PIMAnalyzer()
        assignments = analyzer.get_active_assignments()
        return {"count": len(assignments), "assignments": assignments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assignments/user/{principal_id}/eligible")
async def get_user_eligible_roles(principal_id: str):
    """Get eligible roles for a user"""
    try:
        activator = PIMActivator()
        roles = activator.get_my_eligible_roles(principal_id)
        return {"count": len(roles), "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assignments/user/{principal_id}/active")
async def get_user_active_roles(principal_id: str):
    """Get active roles for a user"""
    try:
        activator = PIMActivator()
        roles = activator.get_my_active_roles(principal_id)
        return {"count": len(roles), "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/usage")
async def analyze_pim_usage():
    """Analyze PIM usage and compliance"""
    try:
        analyzer = PIMAnalyzer()
        usage = analyzer.analyze_pim_usage()
        return usage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/violations")
async def detect_violations():
    """Detect standing admin access violations"""
    try:
        analyzer = PIMAnalyzer()
        violations = analyzer.detect_standing_admin_access()
        return {"count": len(violations), "violations": violations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/excessive-assignments")
async def check_excessive_assignments(threshold: int = 5):
    """Check for users with excessive role assignments"""
    try:
        analyzer = PIMAnalyzer()
        excessive = analyzer.check_excessive_role_assignments(threshold=threshold)
        return {"count": len(excessive), "excessive_assignments": excessive}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/activation-history")
async def get_activation_history(days: int = 30):
    """Get PIM activation history"""
    try:
        analyzer = PIMAnalyzer()
        history = analyzer.get_pim_activation_history(days=days)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_pim_recommendations():
    """Get PIM best practice recommendations"""
    try:
        analyzer = PIMAnalyzer()
        recommendations = analyzer.generate_pim_recommendations()
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/activate")
async def activate_role(request: ActivateRoleRequest):
    """Activate a PIM role"""
    try:
        activator = PIMActivator()
        result = activator.activate_role(
            principal_id=request.principal_id,
            role_definition_id=request.role_definition_id,
            justification=request.justification,
            duration_hours=request.duration_hours,
            ticket_number=request.ticket_number
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deactivate")
async def deactivate_role(request: DeactivateRoleRequest):
    """Deactivate a PIM role"""
    try:
        activator = PIMActivator()
        result = activator.deactivate_role(
            principal_id=request.principal_id,
            role_definition_id=request.role_definition_id,
            justification=request.justification
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activation/{request_id}/status")
async def check_activation_status(request_id: str):
    """Check status of an activation request"""
    try:
        activator = PIMActivator()
        status = activator.check_activation_status(request_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
