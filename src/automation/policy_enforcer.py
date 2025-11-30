"""
Conditional Access Policy Enforcer
Automates policy creation, updates, and enforcement
"""

import logging
from typing import Dict, Any, List, Optional

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class PolicyEnforcer:
    """
    Automates Conditional Access policy management and enforcement
    """

    def __init__(self, use_beta: bool = False):
        """
        Initialize policy enforcer

        Args:
            use_beta: Use Graph API beta endpoint
        """
        self.client = GraphClient(use_beta=use_beta)

    def create_mfa_policy(
        self,
        display_name: str,
        include_users: List[str] = None,
        include_groups: List[str] = None,
        exclude_users: List[str] = None,
        cloud_apps: List[str] = None,
        state: str = "enabledForReportingButNotEnforced"
    ) -> Dict[str, Any]:
        """
        Create a Conditional Access policy requiring MFA

        Args:
            display_name: Policy name
            include_users: User IDs to include (use ["All"] for all users)
            include_groups: Group IDs to include
            exclude_users: User IDs to exclude
            cloud_apps: Application IDs (use ["All"] for all apps)
            state: Policy state (enabled, disabled, enabledForReportingButNotEnforced)

        Returns:
            Created policy object
        """
        logger.info(f"Creating MFA policy: {display_name}")

        request_body = {
            "displayName": display_name,
            "state": state,
            "conditions": {
                "users": {
                    "includeUsers": include_users or ["All"],
                    "includeGroups": include_groups or [],
                    "excludeUsers": exclude_users or []
                },
                "applications": {
                    "includeApplications": cloud_apps or ["All"]
                },
                "clientAppTypes": ["all"]
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["mfa"]
            }
        }

        try:
            response = self.client.post(
                "identity/conditionalAccess/policies",
                request_body
            )

            logger.info(f"MFA policy created successfully: {response.get('id')}")
            return {
                "success": True,
                "policy_id": response.get("id"),
                "display_name": response.get("displayName"),
                "state": response.get("state")
            }

        except GraphAPIError as e:
            logger.error(f"Failed to create MFA policy: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_block_legacy_auth_policy(
        self,
        display_name: str = "Block Legacy Authentication",
        exclude_users: List[str] = None,
        state: str = "enabledForReportingButNotEnforced"
    ) -> Dict[str, Any]:
        """
        Create policy to block legacy authentication protocols

        Args:
            display_name: Policy name
            exclude_users: Users to exclude from policy
            state: Policy state

        Returns:
            Created policy object
        """
        logger.info(f"Creating legacy auth block policy: {display_name}")

        request_body = {
            "displayName": display_name,
            "state": state,
            "conditions": {
                "users": {
                    "includeUsers": ["All"],
                    "excludeUsers": exclude_users or []
                },
                "applications": {
                    "includeApplications": ["All"]
                },
                "clientAppTypes": [
                    "exchangeActiveSync",
                    "other"
                ]
            },
            "grantControls": {
                "operator": "OR",
                "builtInControls": ["block"]
            }
        }

        try:
            response = self.client.post(
                "identity/conditionalAccess/policies",
                request_body
            )

            logger.info(f"Legacy auth block policy created: {response.get('id')}")
            return {
                "success": True,
                "policy_id": response.get("id"),
                "display_name": response.get("displayName")
            }

        except GraphAPIError as e:
            logger.error(f"Failed to create legacy auth block policy: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_compliant_device_policy(
        self,
        display_name: str,
        include_users: List[str] = None,
        include_groups: List[str] = None,
        cloud_apps: List[str] = None,
        platforms: List[str] = None,
        state: str = "enabledForReportingButNotEnforced"
    ) -> Dict[str, Any]:
        """
        Create policy requiring compliant or domain-joined devices

        Args:
            display_name: Policy name
            include_users: Users to include
            include_groups: Groups to include
            cloud_apps: Applications to protect
            platforms: Device platforms (windows, iOS, android, etc.)
            state: Policy state

        Returns:
            Created policy object
        """
        logger.info(f"Creating compliant device policy: {display_name}")

        conditions = {
            "users": {
                "includeUsers": include_users or ["All"],
                "includeGroups": include_groups or []
            },
            "applications": {
                "includeApplications": cloud_apps or ["All"]
            },
            "clientAppTypes": ["all"]
        }

        # Add platform filter if specified
        if platforms:
            conditions["platforms"] = {
                "includePlatforms": platforms
            }

        request_body = {
            "displayName": display_name,
            "state": state,
            "conditions": conditions,
            "grantControls": {
                "operator": "OR",
                "builtInControls": [
                    "compliantDevice",
                    "domainJoinedDevice"
                ]
            }
        }

        try:
            response = self.client.post(
                "identity/conditionalAccess/policies",
                request_body
            )

            logger.info(f"Compliant device policy created: {response.get('id')}")
            return {
                "success": True,
                "policy_id": response.get("id"),
                "display_name": response.get("displayName")
            }

        except GraphAPIError as e:
            logger.error(f"Failed to create compliant device policy: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def update_policy_state(
        self,
        policy_id: str,
        state: str
    ) -> Dict[str, Any]:
        """
        Update policy state (enable, disable, report-only)

        Args:
            policy_id: Policy ID to update
            state: New state (enabled, disabled, enabledForReportingButNotEnforced)

        Returns:
            Update response
        """
        logger.info(f"Updating policy {policy_id} state to {state}")

        request_body = {
            "state": state
        }

        try:
            response = self.client.patch(
                f"identity/conditionalAccess/policies/{policy_id}",
                request_body
            )

            return {
                "success": True,
                "policy_id": policy_id,
                "new_state": state
            }

        except GraphAPIError as e:
            logger.error(f"Failed to update policy state: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def enable_policy(self, policy_id: str) -> Dict[str, Any]:
        """Enable a Conditional Access policy"""
        return self.update_policy_state(policy_id, "enabled")

    def disable_policy(self, policy_id: str) -> Dict[str, Any]:
        """Disable a Conditional Access policy"""
        return self.update_policy_state(policy_id, "disabled")

    def set_report_only(self, policy_id: str) -> Dict[str, Any]:
        """Set policy to report-only mode"""
        return self.update_policy_state(policy_id, "enabledForReportingButNotEnforced")

    def delete_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Delete a Conditional Access policy

        Args:
            policy_id: Policy ID to delete

        Returns:
            Deletion response
        """
        logger.info(f"Deleting policy {policy_id}")

        try:
            self.client.delete(f"identity/conditionalAccess/policies/{policy_id}")

            return {
                "success": True,
                "policy_id": policy_id,
                "deleted": True
            }

        except GraphAPIError as e:
            logger.error(f"Failed to delete policy: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def clone_policy(
        self,
        source_policy_id: str,
        new_display_name: str,
        state: str = "disabled"
    ) -> Dict[str, Any]:
        """
        Clone an existing policy

        Args:
            source_policy_id: Policy to clone
            new_display_name: Name for cloned policy
            state: Initial state for cloned policy

        Returns:
            Cloned policy object
        """
        logger.info(f"Cloning policy {source_policy_id}")

        try:
            # Get source policy
            source = self.client.get(
                f"identity/conditionalAccess/policies/{source_policy_id}"
            )

            # Remove ID and update name/state
            clone_body = {
                "displayName": new_display_name,
                "state": state,
                "conditions": source.get("conditions"),
                "grantControls": source.get("grantControls"),
                "sessionControls": source.get("sessionControls")
            }

            # Create new policy
            response = self.client.post(
                "identity/conditionalAccess/policies",
                clone_body
            )

            logger.info(f"Policy cloned successfully: {response.get('id')}")
            return {
                "success": True,
                "policy_id": response.get("id"),
                "display_name": response.get("displayName"),
                "source_policy_id": source_policy_id
            }

        except GraphAPIError as e:
            logger.error(f"Failed to clone policy: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def bulk_enable_policies(self, policy_ids: List[str]) -> Dict[str, Any]:
        """
        Enable multiple policies

        Args:
            policy_ids: List of policy IDs to enable

        Returns:
            Bulk operation results
        """
        results = {
            "successful": [],
            "failed": [],
            "total": len(policy_ids)
        }

        for policy_id in policy_ids:
            result = self.enable_policy(policy_id)

            if result.get("success"):
                results["successful"].append(policy_id)
            else:
                results["failed"].append({
                    "policy_id": policy_id,
                    "error": result.get("error")
                })

        logger.info(
            f"Bulk enable complete: {len(results['successful'])} succeeded, "
            f"{len(results['failed'])} failed"
        )

        return results

    def add_exclusion_to_policy(
        self,
        policy_id: str,
        exclude_users: List[str] = None,
        exclude_groups: List[str] = None
    ) -> Dict[str, Any]:
        """
        Add exclusions to an existing policy

        Args:
            policy_id: Policy to update
            exclude_users: User IDs to exclude
            exclude_groups: Group IDs to exclude

        Returns:
            Update response
        """
        logger.info(f"Adding exclusions to policy {policy_id}")

        try:
            # Get current policy
            policy = self.client.get(
                f"identity/conditionalAccess/policies/{policy_id}"
            )

            # Update exclusions
            conditions = policy.get("conditions", {})
            users = conditions.get("users", {})

            current_exclude_users = users.get("excludeUsers", [])
            current_exclude_groups = users.get("excludeGroups", [])

            if exclude_users:
                current_exclude_users.extend(exclude_users)

            if exclude_groups:
                current_exclude_groups.extend(exclude_groups)

            # Remove duplicates
            users["excludeUsers"] = list(set(current_exclude_users))
            users["excludeGroups"] = list(set(current_exclude_groups))

            # Update policy
            update_body = {"conditions": conditions}
            response = self.client.patch(
                f"identity/conditionalAccess/policies/{policy_id}",
                update_body
            )

            return {
                "success": True,
                "policy_id": policy_id,
                "exclusions_added": True
            }

        except GraphAPIError as e:
            logger.error(f"Failed to add exclusions: {e}")
            return {
                "success": False,
                "error": str(e)
            }
