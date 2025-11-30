"""
Conditional Access Policy Analyzer
Analyzes CA policies for coverage, conflicts, and security posture
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class PolicyScore:
    """Scoring system for CA policies"""

    # Scoring weights
    WEIGHTS = {
        "mfa_required": 25,
        "device_compliance": 20,
        "block_legacy_auth": 20,
        "location_filtering": 15,
        "app_protection": 10,
        "session_controls": 10
    }

    @classmethod
    def calculate_policy_score(cls, policy: Dict[str, Any]) -> int:
        """
        Calculate security score for a CA policy (0-100)

        Args:
            policy: Conditional Access policy object

        Returns:
            Score from 0 to 100
        """
        score = 0
        conditions = policy.get("conditions", {})
        grant_controls = policy.get("grantControls", {})
        session_controls = policy.get("sessionControls", {})

        # MFA requirement
        built_in_controls = grant_controls.get("builtInControls", [])
        if "mfa" in built_in_controls or "mfaFromOtherProvider" in built_in_controls:
            score += cls.WEIGHTS["mfa_required"]

        # Device compliance
        if "compliantDevice" in built_in_controls or "domainJoinedDevice" in built_in_controls:
            score += cls.WEIGHTS["device_compliance"]

        # Block legacy authentication
        client_app_types = conditions.get("clientAppTypes", [])
        if "exchangeActiveSync" in client_app_types or "other" in client_app_types:
            if grant_controls.get("operator") == "OR":
                score += cls.WEIGHTS["block_legacy_auth"] // 2
        else:
            score += cls.WEIGHTS["block_legacy_auth"]

        # Location-based filtering
        locations = conditions.get("locations", {})
        if locations.get("includeLocations") or locations.get("excludeLocations"):
            score += cls.WEIGHTS["location_filtering"]

        # App protection policies
        if "approvedApplication" in built_in_controls or "compliantApplication" in built_in_controls:
            score += cls.WEIGHTS["app_protection"]

        # Session controls
        if session_controls:
            score += cls.WEIGHTS["session_controls"]

        return min(score, 100)


class ConditionalAccessAnalyzer:
    """
    Analyzes Conditional Access policies for security and governance
    """

    def __init__(self, use_beta: bool = False):
        """
        Initialize CA analyzer

        Args:
            use_beta: Use Graph API beta endpoint
        """
        self.client = GraphClient(use_beta=use_beta)

    def get_all_policies(self) -> List[Dict[str, Any]]:
        """
        Retrieve all Conditional Access policies

        Returns:
            List of CA policy objects
        """
        try:
            logger.info("Fetching all Conditional Access policies")
            policies = self.client.get_all_pages("identity/conditionalAccess/policies")
            logger.info(f"Retrieved {len(policies)} CA policies")
            return policies
        except GraphAPIError as e:
            logger.error(f"Failed to fetch CA policies: {e}")
            raise

    def get_policy_by_id(self, policy_id: str) -> Dict[str, Any]:
        """
        Get specific CA policy by ID

        Args:
            policy_id: Policy ID

        Returns:
            CA policy object
        """
        return self.client.get(f"identity/conditionalAccess/policies/{policy_id}")

    def analyze_policy_coverage(self, policies: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Analyze coverage of CA policies

        Args:
            policies: List of policies (fetches if not provided)

        Returns:
            Coverage analysis report
        """
        if policies is None:
            policies = self.get_all_policies()

        enabled_policies = [p for p in policies if p.get("state") == "enabled"]
        disabled_policies = [p for p in policies if p.get("state") == "disabled"]
        report_only_policies = [p for p in policies if p.get("state") == "enabledForReportingButNotEnforced"]

        # Analyze what's protected
        protected_apps = set()
        protected_users = set()
        requires_mfa = []
        blocks_legacy_auth = []

        for policy in enabled_policies:
            conditions = policy.get("conditions", {})
            grant_controls = policy.get("grantControls", {})

            # Apps
            app_condition = conditions.get("applications", {})
            if app_condition.get("includeApplications"):
                protected_apps.update(app_condition["includeApplications"])

            # Users
            user_condition = conditions.get("users", {})
            if user_condition.get("includeUsers"):
                protected_users.update(user_condition["includeUsers"])

            # Controls
            built_in_controls = grant_controls.get("builtInControls", [])
            if "mfa" in built_in_controls:
                requires_mfa.append(policy["displayName"])

            client_app_types = conditions.get("clientAppTypes", [])
            if "exchangeActiveSync" in client_app_types or "other" in client_app_types:
                blocks_legacy_auth.append(policy["displayName"])

        return {
            "summary": {
                "total_policies": len(policies),
                "enabled": len(enabled_policies),
                "disabled": len(disabled_policies),
                "report_only": len(report_only_policies)
            },
            "coverage": {
                "protected_applications": len(protected_apps),
                "protected_users": len(protected_users),
                "all_apps_protected": "All" in protected_apps,
                "all_users_protected": "All" in protected_users
            },
            "security_controls": {
                "mfa_policies": len(requires_mfa),
                "legacy_auth_blocks": len(blocks_legacy_auth),
                "mfa_policy_names": requires_mfa,
                "legacy_auth_policy_names": blocks_legacy_auth
            },
            "timestamp": datetime.utcnow().isoformat()
        }

    def detect_policy_conflicts(self, policies: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Detect conflicting CA policies

        Args:
            policies: List of policies (fetches if not provided)

        Returns:
            List of potential conflicts
        """
        if policies is None:
            policies = self.get_all_policies()

        conflicts = []
        enabled_policies = [p for p in policies if p.get("state") == "enabled"]

        # Group policies by similar conditions
        policy_groups = defaultdict(list)

        for policy in enabled_policies:
            conditions = policy.get("conditions", {})
            users = frozenset(conditions.get("users", {}).get("includeUsers", []))
            apps = frozenset(conditions.get("applications", {}).get("includeApplications", []))

            key = (users, apps)
            policy_groups[key].append(policy)

        # Check for conflicting grant controls in same scope
        for key, group_policies in policy_groups.items():
            if len(group_policies) > 1:
                for i, policy1 in enumerate(group_policies):
                    for policy2 in group_policies[i + 1:]:
                        grant1 = policy1.get("grantControls", {})
                        grant2 = policy2.get("grantControls", {})

                        # Check for block vs allow conflict
                        if grant1.get("operator") == "AND" and grant2.get("operator") == "OR":
                            conflicts.append({
                                "type": "grant_control_conflict",
                                "severity": "medium",
                                "policy1": policy1["displayName"],
                                "policy2": policy2["displayName"],
                                "description": "Policies have different grant control operators (AND vs OR)"
                            })

        return conflicts

    def score_all_policies(self, policies: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Score all CA policies for security strength

        Args:
            policies: List of policies (fetches if not provided)

        Returns:
            Scoring report with recommendations
        """
        if policies is None:
            policies = self.get_all_policies()

        scored_policies = []
        total_score = 0

        for policy in policies:
            if policy.get("state") == "enabled":
                score = PolicyScore.calculate_policy_score(policy)
                scored_policies.append({
                    "id": policy["id"],
                    "displayName": policy["displayName"],
                    "score": score,
                    "state": policy["state"]
                })
                total_score += score

        scored_policies.sort(key=lambda x: x["score"], reverse=True)

        avg_score = total_score / len(scored_policies) if scored_policies else 0

        recommendations = []
        if avg_score < 60:
            recommendations.append("Overall CA security posture is weak. Consider implementing MFA and device compliance.")
        if avg_score < 80:
            recommendations.append("Good foundation, but consider adding location-based controls and app protection policies.")

        weak_policies = [p for p in scored_policies if p["score"] < 50]
        if weak_policies:
            recommendations.append(f"{len(weak_policies)} policies have weak security controls. Review: {', '.join([p['displayName'] for p in weak_policies[:3]])}")

        return {
            "average_score": round(avg_score, 2),
            "total_policies_scored": len(scored_policies),
            "policies": scored_policies,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_recommendations(self, policies: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Generate security recommendations based on CA policy analysis

        Args:
            policies: List of policies (fetches if not provided)

        Returns:
            List of recommendations
        """
        if policies is None:
            policies = self.get_all_policies()

        recommendations = []
        enabled_policies = [p for p in policies if p.get("state") == "enabled"]

        # Check for basic security controls
        has_mfa = any(
            "mfa" in p.get("grantControls", {}).get("builtInControls", [])
            for p in enabled_policies
        )

        has_legacy_auth_block = any(
            "exchangeActiveSync" in p.get("conditions", {}).get("clientAppTypes", [])
            for p in enabled_policies
        )

        has_device_compliance = any(
            "compliantDevice" in p.get("grantControls", {}).get("builtInControls", [])
            for p in enabled_policies
        )

        if not has_mfa:
            recommendations.append("CRITICAL: No MFA policies detected. Implement MFA for all users or high-risk scenarios.")

        if not has_legacy_auth_block:
            recommendations.append("HIGH: Legacy authentication protocols are not blocked. Create policy to block legacy auth.")

        if not has_device_compliance:
            recommendations.append("MEDIUM: No device compliance checks detected. Consider requiring compliant devices.")

        if len(enabled_policies) < 3:
            recommendations.append("LOW: Only {len(enabled_policies)} policies enabled. Consider implementing more granular controls.")

        # Check for report-only policies
        report_only = [p for p in policies if p.get("state") == "enabledForReportingButNotEnforced"]
        if report_only:
            recommendations.append(f"INFO: {len(report_only)} policies in report-only mode. Review for enforcement.")

        return recommendations
