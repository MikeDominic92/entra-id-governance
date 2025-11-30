"""
Conditional Access Policy API Routes
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from ...analyzers import ConditionalAccessAnalyzer
from ...automation import PolicyEnforcer

router = APIRouter()


class CreateMFAPolicyRequest(BaseModel):
    """Request model for creating MFA policy"""
    display_name: str
    include_users: List[str] = ["All"]
    include_groups: List[str] = []
    exclude_users: List[str] = []
    cloud_apps: List[str] = ["All"]
    state: str = "enabledForReportingButNotEnforced"


class UpdatePolicyStateRequest(BaseModel):
    """Request model for updating policy state"""
    state: str  # enabled, disabled, enabledForReportingButNotEnforced


@router.get("/")
async def get_all_policies():
    """Get all Conditional Access policies"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        policies = analyzer.get_all_policies()
        return {"count": len(policies), "policies": policies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{policy_id}")
async def get_policy(policy_id: str):
    """Get specific policy by ID"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        policy = analyzer.get_policy_by_id(policy_id)
        return policy
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/analysis/coverage")
async def analyze_coverage():
    """Analyze Conditional Access policy coverage"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        coverage = analyzer.analyze_policy_coverage()
        return coverage
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/conflicts")
async def detect_conflicts():
    """Detect conflicting policies"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        conflicts = analyzer.detect_policy_conflicts()
        return {"count": len(conflicts), "conflicts": conflicts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/scores")
async def score_policies():
    """Score all policies for security strength"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        scores = analyzer.score_all_policies()
        return scores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_recommendations():
    """Get policy recommendations"""
    try:
        analyzer = ConditionalAccessAnalyzer()
        recommendations = analyzer.generate_recommendations()
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create/mfa")
async def create_mfa_policy(request: CreateMFAPolicyRequest):
    """Create MFA policy"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.create_mfa_policy(
            display_name=request.display_name,
            include_users=request.include_users,
            include_groups=request.include_groups,
            exclude_users=request.exclude_users,
            cloud_apps=request.cloud_apps,
            state=request.state
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create/block-legacy-auth")
async def create_block_legacy_auth():
    """Create policy to block legacy authentication"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.create_block_legacy_auth_policy()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{policy_id}/state")
async def update_policy_state(policy_id: str, request: UpdatePolicyStateRequest):
    """Update policy state"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.update_policy_state(policy_id, request.state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{policy_id}/enable")
async def enable_policy(policy_id: str):
    """Enable a policy"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.enable_policy(policy_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{policy_id}/disable")
async def disable_policy(policy_id: str):
    """Disable a policy"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.disable_policy(policy_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{policy_id}")
async def delete_policy(policy_id: str):
    """Delete a policy"""
    try:
        enforcer = PolicyEnforcer()
        result = enforcer.delete_policy(policy_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
