"""
PIM Role Activation Automation
Automates activation and management of PIM roles
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class PIMActivator:
    """
    Automates PIM role activation and deactivation
    """

    def __init__(self, use_beta: bool = True):
        """
        Initialize PIM activator

        Args:
            use_beta: Use Graph API beta endpoint (required for PIM)
        """
        self.client = GraphClient(use_beta=use_beta)

    def activate_role(
        self,
        principal_id: str,
        role_definition_id: str,
        justification: str,
        duration_hours: int = 8,
        ticket_number: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Activate a PIM eligible role

        Args:
            principal_id: User principal ID
            role_definition_id: Role definition ID to activate
            justification: Business justification for activation
            duration_hours: Activation duration (default 8 hours)
            ticket_number: Optional ticket/incident number

        Returns:
            Activation request response

        Raises:
            GraphAPIError: If activation fails
        """
        logger.info(
            f"Activating role {role_definition_id} for principal {principal_id}"
        )

        # Calculate expiration
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=duration_hours)

        request_body = {
            "action": "selfActivate",
            "principalId": principal_id,
            "roleDefinitionId": role_definition_id,
            "directoryScopeId": "/",
            "justification": justification,
            "scheduleInfo": {
                "startDateTime": start_time.isoformat() + "Z",
                "expiration": {
                    "type": "afterDuration",
                    "duration": f"PT{duration_hours}H",
                },
            },
        }

        # Add ticket number if provided
        if ticket_number:
            request_body["ticketInfo"] = {
                "ticketNumber": ticket_number,
                "ticketSystem": "ServiceNow",  # Customize as needed
            }

        try:
            response = self.client.post(
                "roleManagement/directory/roleAssignmentScheduleRequests", request_body
            )

            logger.info(f"Role activation successful: {response.get('id')}")
            return {
                "success": True,
                "request_id": response.get("id"),
                "status": response.get("status"),
                "created_datetime": response.get("createdDateTime"),
                "activation_duration_hours": duration_hours,
                "expires_at": end_time.isoformat(),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to activate role: {e}")
            return {"success": False, "error": str(e)}

    def deactivate_role(
        self,
        principal_id: str,
        role_definition_id: str,
        justification: str = "Manual deactivation",
    ) -> Dict[str, Any]:
        """
        Deactivate an active PIM role

        Args:
            principal_id: User principal ID
            role_definition_id: Role definition ID to deactivate
            justification: Reason for deactivation

        Returns:
            Deactivation response
        """
        logger.info(
            f"Deactivating role {role_definition_id} for principal {principal_id}"
        )

        request_body = {
            "action": "selfDeactivate",
            "principalId": principal_id,
            "roleDefinitionId": role_definition_id,
            "directoryScopeId": "/",
            "justification": justification,
        }

        try:
            response = self.client.post(
                "roleManagement/directory/roleAssignmentScheduleRequests", request_body
            )

            logger.info(f"Role deactivation successful: {response.get('id')}")
            return {
                "success": True,
                "request_id": response.get("id"),
                "status": response.get("status"),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to deactivate role: {e}")
            return {"success": False, "error": str(e)}

    def extend_activation(
        self,
        assignment_id: str,
        additional_hours: int = 4,
        justification: str = "Extension required",
    ) -> Dict[str, Any]:
        """
        Extend an active role assignment

        Args:
            assignment_id: Active assignment ID
            additional_hours: Hours to extend by
            justification: Reason for extension

        Returns:
            Extension response
        """
        logger.info(f"Extending assignment {assignment_id} by {additional_hours} hours")

        # Get current assignment details
        try:
            assignment = self.client.get(
                f"roleManagement/directory/roleAssignmentScheduleInstances/{assignment_id}"
            )

            # Create extension request
            request_body = {
                "action": "adminExtend",
                "principalId": assignment.get("principalId"),
                "roleDefinitionId": assignment.get("roleDefinitionId"),
                "directoryScopeId": "/",
                "justification": justification,
                "scheduleInfo": {
                    "expiration": {
                        "type": "afterDuration",
                        "duration": f"PT{additional_hours}H",
                    }
                },
            }

            response = self.client.post(
                "roleManagement/directory/roleAssignmentScheduleRequests", request_body
            )

            return {
                "success": True,
                "request_id": response.get("id"),
                "extended_hours": additional_hours,
            }

        except GraphAPIError as e:
            logger.error(f"Failed to extend activation: {e}")
            return {"success": False, "error": str(e)}

    def get_my_eligible_roles(self, principal_id: str) -> list[Dict[str, Any]]:
        """
        Get all eligible roles for a principal

        Args:
            principal_id: User principal ID

        Returns:
            List of eligible role assignments
        """
        try:
            filter_query = f"principalId eq '{principal_id}'"
            eligible_roles = self.client.get_all_pages(
                "roleManagement/directory/roleEligibilityScheduleInstances",
                params={"$filter": filter_query},
            )

            logger.info(
                f"Found {len(eligible_roles)} eligible roles for {principal_id}"
            )
            return eligible_roles

        except GraphAPIError as e:
            logger.error(f"Failed to get eligible roles: {e}")
            return []

    def get_my_active_roles(self, principal_id: str) -> list[Dict[str, Any]]:
        """
        Get all active roles for a principal

        Args:
            principal_id: User principal ID

        Returns:
            List of active role assignments
        """
        try:
            filter_query = f"principalId eq '{principal_id}'"
            active_roles = self.client.get_all_pages(
                "roleManagement/directory/roleAssignmentScheduleInstances",
                params={"$filter": filter_query},
            )

            logger.info(f"Found {len(active_roles)} active roles for {principal_id}")
            return active_roles

        except GraphAPIError as e:
            logger.error(f"Failed to get active roles: {e}")
            return []

    def check_activation_status(self, request_id: str) -> Dict[str, Any]:
        """
        Check status of an activation request

        Args:
            request_id: Activation request ID

        Returns:
            Request status information
        """
        try:
            request = self.client.get(
                f"roleManagement/directory/roleAssignmentScheduleRequests/{request_id}"
            )

            return {
                "request_id": request_id,
                "status": request.get("status"),
                "action": request.get("action"),
                "created_datetime": request.get("createdDateTime"),
                "completed_datetime": request.get("completedDateTime"),
                "approval_required": request.get("isValidationOnly", False),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to check activation status: {e}")
            return {"request_id": request_id, "error": str(e)}

    def bulk_activate_roles(self, activations: list[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Activate multiple roles in batch

        Args:
            activations: List of activation requests with principal_id, role_definition_id, justification

        Returns:
            Batch activation results
        """
        results = {"successful": [], "failed": [], "total": len(activations)}

        for activation in activations:
            result = self.activate_role(
                principal_id=activation["principal_id"],
                role_definition_id=activation["role_definition_id"],
                justification=activation.get("justification", "Bulk activation"),
                duration_hours=activation.get("duration_hours", 8),
                ticket_number=activation.get("ticket_number"),
            )

            if result.get("success"):
                results["successful"].append(result)
            else:
                results["failed"].append(
                    {"activation": activation, "error": result.get("error")}
                )

        logger.info(
            f"Bulk activation complete: {len(results['successful'])} succeeded, "
            f"{len(results['failed'])} failed"
        )

        return results

    def schedule_activation(
        self,
        principal_id: str,
        role_definition_id: str,
        justification: str,
        start_datetime: datetime,
        duration_hours: int = 8,
    ) -> Dict[str, Any]:
        """
        Schedule a future role activation

        Args:
            principal_id: User principal ID
            role_definition_id: Role to activate
            justification: Business justification
            start_datetime: When to activate the role
            duration_hours: How long to keep active

        Returns:
            Scheduling response
        """
        logger.info(f"Scheduling role activation for {start_datetime}")

        end_time = start_datetime + timedelta(hours=duration_hours)

        request_body = {
            "action": "adminAssign",
            "principalId": principal_id,
            "roleDefinitionId": role_definition_id,
            "directoryScopeId": "/",
            "justification": justification,
            "scheduleInfo": {
                "startDateTime": start_datetime.isoformat() + "Z",
                "expiration": {
                    "type": "afterDateTime",
                    "endDateTime": end_time.isoformat() + "Z",
                },
            },
        }

        try:
            response = self.client.post(
                "roleManagement/directory/roleAssignmentScheduleRequests", request_body
            )

            return {
                "success": True,
                "request_id": response.get("id"),
                "scheduled_for": start_datetime.isoformat(),
                "expires_at": end_time.isoformat(),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to schedule activation: {e}")
            return {"success": False, "error": str(e)}
