"""
Privileged Identity Management (PIM) Analyzer
Analyzes PIM role assignments and ensures just-in-time access compliance
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class PIMAnalyzer:
    """
    Analyzes PIM role assignments for security and compliance
    """

    # High-privilege roles that should always use PIM
    CRITICAL_ROLES = [
        "Global Administrator",
        "Privileged Role Administrator",
        "Security Administrator",
        "Exchange Administrator",
        "SharePoint Administrator",
        "User Administrator",
        "Application Administrator",
        "Cloud Application Administrator"
    ]

    def __init__(self, use_beta: bool = True):
        """
        Initialize PIM analyzer

        Args:
            use_beta: Use Graph API beta endpoint (required for PIM)
        """
        self.client = GraphClient(use_beta=use_beta)

    def get_role_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all directory role definitions

        Returns:
            List of role definition objects
        """
        try:
            logger.info("Fetching directory role definitions")
            roles = self.client.get_all_pages("roleManagement/directory/roleDefinitions")
            logger.info(f"Retrieved {len(roles)} role definitions")
            return roles
        except GraphAPIError as e:
            logger.error(f"Failed to fetch role definitions: {e}")
            raise

    def get_eligible_assignments(self) -> List[Dict[str, Any]]:
        """
        Get all eligible (PIM) role assignments

        Returns:
            List of eligible assignment objects
        """
        try:
            logger.info("Fetching eligible role assignments")
            assignments = self.client.get_all_pages(
                "roleManagement/directory/roleEligibilityScheduleInstances"
            )
            logger.info(f"Retrieved {len(assignments)} eligible assignments")
            return assignments
        except GraphAPIError as e:
            logger.error(f"Failed to fetch eligible assignments: {e}")
            raise

    def get_active_assignments(self) -> List[Dict[str, Any]]:
        """
        Get all active (standing) role assignments

        Returns:
            List of active assignment objects
        """
        try:
            logger.info("Fetching active role assignments")
            assignments = self.client.get_all_pages(
                "roleManagement/directory/roleAssignmentScheduleInstances"
            )
            logger.info(f"Retrieved {len(assignments)} active assignments")
            return assignments
        except GraphAPIError as e:
            logger.error(f"Failed to fetch active assignments: {e}")
            raise

    def get_role_assignment_requests(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get PIM activation requests from the last N days

        Args:
            days: Number of days to look back

        Returns:
            List of activation request objects
        """
        try:
            logger.info(f"Fetching role assignment requests from last {days} days")

            # Calculate date filter
            start_date = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
            filter_query = f"createdDateTime ge {start_date}"

            requests = self.client.get_all_pages(
                "roleManagement/directory/roleAssignmentScheduleRequests",
                params={"$filter": filter_query}
            )
            logger.info(f"Retrieved {len(requests)} activation requests")
            return requests
        except GraphAPIError as e:
            logger.error(f"Failed to fetch activation requests: {e}")
            return []

    def detect_standing_admin_access(
        self,
        active_assignments: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect standing (permanent) administrator access - a security violation

        Args:
            active_assignments: List of active assignments (fetches if not provided)

        Returns:
            List of violations with details
        """
        if active_assignments is None:
            active_assignments = self.get_active_assignments()

        role_definitions = self.get_role_definitions()
        role_map = {role["id"]: role["displayName"] for role in role_definitions}

        violations = []

        for assignment in active_assignments:
            role_id = assignment.get("roleDefinitionId")
            role_name = role_map.get(role_id, "Unknown Role")

            # Check if this is a critical role with standing access
            if role_name in self.CRITICAL_ROLES:
                # Check if assignment is permanent (no end date or far future)
                end_date_time = assignment.get("endDateTime")

                is_permanent = False
                if not end_date_time:
                    is_permanent = True
                else:
                    # If end date is more than 1 year away, consider it permanent
                    try:
                        end_date = datetime.fromisoformat(end_date_time.replace("Z", "+00:00"))
                        if (end_date - datetime.now(end_date.tzinfo)).days > 365:
                            is_permanent = True
                    except:
                        pass

                if is_permanent:
                    violations.append({
                        "principal_id": assignment.get("principalId"),
                        "role_name": role_name,
                        "role_id": role_id,
                        "assignment_id": assignment.get("id"),
                        "severity": "HIGH",
                        "description": f"Standing access to {role_name} detected. Should use PIM eligible assignment instead.",
                        "recommendation": "Convert to PIM eligible assignment with just-in-time activation"
                    })

        logger.info(f"Detected {len(violations)} standing admin access violations")
        return violations

    def analyze_pim_usage(
        self,
        eligible_assignments: Optional[List[Dict[str, Any]]] = None,
        active_assignments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze overall PIM usage and compliance

        Args:
            eligible_assignments: List of eligible assignments
            active_assignments: List of active assignments

        Returns:
            Analysis report
        """
        if eligible_assignments is None:
            eligible_assignments = self.get_eligible_assignments()

        if active_assignments is None:
            active_assignments = self.get_active_assignments()

        role_definitions = self.get_role_definitions()
        role_map = {role["id"]: role["displayName"] for role in role_definitions}

        # Count assignments by role
        eligible_by_role = Counter()
        active_by_role = Counter()

        for assignment in eligible_assignments:
            role_id = assignment.get("roleDefinitionId")
            role_name = role_map.get(role_id, "Unknown")
            eligible_by_role[role_name] += 1

        for assignment in active_assignments:
            role_id = assignment.get("roleDefinitionId")
            role_name = role_map.get(role_id, "Unknown")
            active_by_role[role_name] += 1

        # Check PIM adoption for critical roles
        critical_role_stats = {}
        for role_name in self.CRITICAL_ROLES:
            critical_role_stats[role_name] = {
                "eligible": eligible_by_role.get(role_name, 0),
                "active": active_by_role.get(role_name, 0),
                "pim_adoption": eligible_by_role.get(role_name, 0) > 0
            }

        # Calculate compliance score
        roles_using_pim = sum(1 for stats in critical_role_stats.values() if stats["pim_adoption"])
        compliance_score = (roles_using_pim / len(self.CRITICAL_ROLES)) * 100 if self.CRITICAL_ROLES else 0

        return {
            "summary": {
                "total_eligible_assignments": len(eligible_assignments),
                "total_active_assignments": len(active_assignments),
                "unique_roles_with_pim": len(eligible_by_role),
                "compliance_score": round(compliance_score, 2)
            },
            "critical_roles": critical_role_stats,
            "top_eligible_roles": dict(eligible_by_role.most_common(10)),
            "top_active_roles": dict(active_by_role.most_common(10)),
            "timestamp": datetime.utcnow().isoformat()
        }

    def check_excessive_role_assignments(
        self,
        eligible_assignments: Optional[List[Dict[str, Any]]] = None,
        threshold: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Detect users with excessive role assignments

        Args:
            eligible_assignments: List of eligible assignments
            threshold: Number of roles that triggers alert

        Returns:
            List of users with excessive assignments
        """
        if eligible_assignments is None:
            eligible_assignments = self.get_eligible_assignments()

        # Count roles per user
        user_role_count = Counter()
        user_roles = {}

        role_definitions = self.get_role_definitions()
        role_map = {role["id"]: role["displayName"] for role in role_definitions}

        for assignment in eligible_assignments:
            principal_id = assignment.get("principalId")
            role_id = assignment.get("roleDefinitionId")
            role_name = role_map.get(role_id, "Unknown")

            user_role_count[principal_id] += 1
            if principal_id not in user_roles:
                user_roles[principal_id] = []
            user_roles[principal_id].append(role_name)

        # Find users exceeding threshold
        excessive_assignments = []
        for principal_id, count in user_role_count.items():
            if count >= threshold:
                excessive_assignments.append({
                    "principal_id": principal_id,
                    "role_count": count,
                    "roles": user_roles[principal_id],
                    "severity": "HIGH" if count >= threshold * 2 else "MEDIUM",
                    "recommendation": "Review if all role assignments are necessary. Apply least privilege principle."
                })

        excessive_assignments.sort(key=lambda x: x["role_count"], reverse=True)
        logger.info(f"Found {len(excessive_assignments)} users with {threshold}+ role assignments")

        return excessive_assignments

    def get_pim_activation_history(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze PIM activation patterns over time

        Args:
            days: Number of days to analyze

        Returns:
            Activation history analysis
        """
        requests = self.get_role_assignment_requests(days)

        # Filter for activation requests
        activations = [
            r for r in requests
            if r.get("action") == "adminAssign" or r.get("action") == "selfActivate"
        ]

        # Count activations by role
        role_definitions = self.get_role_definitions()
        role_map = {role["id"]: role["displayName"] for role in role_definitions}

        activations_by_role = Counter()
        activations_by_user = Counter()

        for activation in activations:
            role_id = activation.get("roleDefinitionId")
            principal_id = activation.get("principalId")

            role_name = role_map.get(role_id, "Unknown")
            activations_by_role[role_name] += 1
            activations_by_user[principal_id] += 1

        return {
            "period_days": days,
            "total_activations": len(activations),
            "unique_users": len(activations_by_user),
            "unique_roles": len(activations_by_role),
            "most_activated_roles": dict(activations_by_role.most_common(10)),
            "most_active_users": dict(activations_by_user.most_common(10)),
            "average_activations_per_day": round(len(activations) / days, 2),
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_pim_recommendations(self) -> List[str]:
        """
        Generate PIM best practice recommendations

        Returns:
            List of recommendations
        """
        recommendations = []

        try:
            # Get data
            eligible = self.get_eligible_assignments()
            active = self.get_active_assignments()
            violations = self.detect_standing_admin_access(active)

            # Check for violations
            if violations:
                recommendations.append(
                    f"CRITICAL: {len(violations)} standing admin assignments detected. "
                    "Convert to PIM eligible assignments immediately."
                )

            # Check PIM adoption
            if len(eligible) == 0:
                recommendations.append(
                    "CRITICAL: No PIM eligible assignments found. "
                    "Implement PIM for privileged roles to enable just-in-time access."
                )
            elif len(eligible) < len(active):
                recommendations.append(
                    f"HIGH: More active ({len(active)}) than eligible ({len(eligible)}) assignments. "
                    "Migrate more roles to PIM eligible assignments."
                )

            # Check for excessive assignments
            excessive = self.check_excessive_role_assignments(eligible, threshold=5)
            if excessive:
                recommendations.append(
                    f"MEDIUM: {len(excessive)} users have 5+ role assignments. "
                    "Review for least privilege compliance."
                )

            # General recommendations
            recommendations.append(
                "INFO: Regularly review PIM activation logs for suspicious activity."
            )
            recommendations.append(
                "INFO: Configure approval workflows for critical role activations."
            )
            recommendations.append(
                "INFO: Set appropriate activation duration limits (recommend 4-8 hours max)."
            )

        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append(f"ERROR: Unable to generate full recommendations: {e}")

        return recommendations
