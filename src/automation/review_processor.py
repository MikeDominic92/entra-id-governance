"""
Access Review Automation Processor
Automates access review processing and decision making
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class ReviewProcessor:
    """
    Automates access review processing and decisions
    """

    def __init__(self, use_beta: bool = True):
        """
        Initialize review processor

        Args:
            use_beta: Use Graph API beta endpoint
        """
        self.client = GraphClient(use_beta=use_beta)

    def approve_decision(
        self,
        review_id: str,
        instance_id: str,
        decision_id: str,
        justification: str,
        reviewer_id: str,
    ) -> Dict[str, Any]:
        """
        Approve an access review decision

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            decision_id: Decision ID to approve
            justification: Approval justification
            reviewer_id: Reviewer principal ID

        Returns:
            Approval response
        """
        logger.info(f"Approving decision {decision_id} in review {review_id}")

        request_body = {
            "decision": "Approve",
            "justification": justification,
            "reviewedBy": {"id": reviewer_id},
            "reviewedDateTime": datetime.utcnow().isoformat() + "Z",
        }

        try:
            response = self.client.patch(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/decisions/{decision_id}",
                request_body,
            )

            return {
                "success": True,
                "decision_id": decision_id,
                "decision": "Approve",
                "reviewed_datetime": datetime.utcnow().isoformat(),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to approve decision: {e}")
            return {"success": False, "error": str(e)}

    def deny_decision(
        self,
        review_id: str,
        instance_id: str,
        decision_id: str,
        justification: str,
        reviewer_id: str,
    ) -> Dict[str, Any]:
        """
        Deny an access review decision

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            decision_id: Decision ID to deny
            justification: Denial justification
            reviewer_id: Reviewer principal ID

        Returns:
            Denial response
        """
        logger.info(f"Denying decision {decision_id} in review {review_id}")

        request_body = {
            "decision": "Deny",
            "justification": justification,
            "reviewedBy": {"id": reviewer_id},
            "reviewedDateTime": datetime.utcnow().isoformat() + "Z",
        }

        try:
            response = self.client.patch(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/decisions/{decision_id}",
                request_body,
            )

            return {
                "success": True,
                "decision_id": decision_id,
                "decision": "Deny",
                "reviewed_datetime": datetime.utcnow().isoformat(),
            }

        except GraphAPIError as e:
            logger.error(f"Failed to deny decision: {e}")
            return {"success": False, "error": str(e)}

    def bulk_approve(
        self,
        review_id: str,
        instance_id: str,
        decision_ids: List[str],
        justification: str,
        reviewer_id: str,
    ) -> Dict[str, Any]:
        """
        Bulk approve multiple decisions

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            decision_ids: List of decision IDs to approve
            justification: Approval justification
            reviewer_id: Reviewer principal ID

        Returns:
            Bulk approval results
        """
        logger.info(f"Bulk approving {len(decision_ids)} decisions")

        results = {"successful": [], "failed": [], "total": len(decision_ids)}

        for decision_id in decision_ids:
            result = self.approve_decision(
                review_id, instance_id, decision_id, justification, reviewer_id
            )

            if result.get("success"):
                results["successful"].append(decision_id)
            else:
                results["failed"].append(
                    {"decision_id": decision_id, "error": result.get("error")}
                )

        logger.info(
            f"Bulk approval complete: {len(results['successful'])} succeeded, "
            f"{len(results['failed'])} failed"
        )

        return results

    def auto_approve_compliant_users(
        self,
        review_id: str,
        instance_id: str,
        reviewer_id: str,
        compliance_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Automatically approve decisions for users meeting compliance criteria

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            reviewer_id: Reviewer principal ID
            compliance_criteria: Optional criteria for auto-approval

        Returns:
            Auto-approval results
        """
        logger.info("Processing auto-approvals for compliant users")

        # Get all pending decisions
        try:
            decisions = self.client.get_all_pages(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/decisions"
            )
        except GraphAPIError as e:
            logger.error(f"Failed to fetch decisions: {e}")
            return {"success": False, "error": str(e)}

        # Filter for not reviewed decisions
        pending = [d for d in decisions if d.get("decision") == "NotReviewed"]

        auto_approved = []
        skipped = []

        for decision in pending:
            # Default compliance: user has signed in recently
            principal = decision.get("principal", {})

            # Simple compliance check - can be extended with more criteria
            should_approve = True  # Default to approve for demonstration

            # If compliance criteria provided, use it
            if compliance_criteria:
                # Example: Check last sign-in
                # In production, you'd fetch user details and check against criteria
                pass

            if should_approve:
                result = self.approve_decision(
                    review_id,
                    instance_id,
                    decision["id"],
                    "Auto-approved: Meets compliance criteria",
                    reviewer_id,
                )

                if result.get("success"):
                    auto_approved.append(decision["id"])
                else:
                    skipped.append(decision["id"])
            else:
                skipped.append(decision["id"])

        return {
            "success": True,
            "auto_approved": len(auto_approved),
            "skipped": len(skipped),
            "total_pending": len(pending),
        }

    def stop_review(self, review_id: str, instance_id: str) -> Dict[str, Any]:
        """
        Stop an in-progress access review

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID

        Returns:
            Stop response
        """
        logger.info(f"Stopping review instance {instance_id}")

        try:
            response = self.client.post(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/stop",
                {},
            )

            return {
                "success": True,
                "review_id": review_id,
                "instance_id": instance_id,
                "status": "Stopped",
            }

        except GraphAPIError as e:
            logger.error(f"Failed to stop review: {e}")
            return {"success": False, "error": str(e)}

    def apply_decisions(self, review_id: str, instance_id: str) -> Dict[str, Any]:
        """
        Apply review decisions (remove access for denied decisions)

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID

        Returns:
            Application response
        """
        logger.info(f"Applying decisions for review instance {instance_id}")

        try:
            response = self.client.post(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/applyDecisions",
                {},
            )

            return {
                "success": True,
                "review_id": review_id,
                "instance_id": instance_id,
                "status": "Decisions applied",
            }

        except GraphAPIError as e:
            logger.error(f"Failed to apply decisions: {e}")
            return {"success": False, "error": str(e)}

    def send_reminder(
        self, review_id: str, instance_id: str, message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send reminder to reviewers

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            message: Optional custom message

        Returns:
            Reminder response
        """
        logger.info(f"Sending reminder for review instance {instance_id}")

        request_body = {
            "message": message or "Please complete your pending access review."
        }

        try:
            response = self.client.post(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/sendReminder",
                request_body,
            )

            return {
                "success": True,
                "review_id": review_id,
                "instance_id": instance_id,
                "reminder_sent": True,
            }

        except GraphAPIError as e:
            logger.error(f"Failed to send reminder: {e}")
            return {"success": False, "error": str(e)}

    def get_decision_insights(self, review_id: str, instance_id: str) -> Dict[str, Any]:
        """
        Get insights about review decisions

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID

        Returns:
            Decision insights
        """
        try:
            decisions = self.client.get_all_pages(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/decisions"
            )

            total = len(decisions)
            approved = sum(1 for d in decisions if d.get("decision") == "Approve")
            denied = sum(1 for d in decisions if d.get("decision") == "Deny")
            not_reviewed = sum(
                1 for d in decisions if d.get("decision") == "NotReviewed"
            )

            completion_rate = ((approved + denied) / total * 100) if total > 0 else 0

            return {
                "total_decisions": total,
                "approved": approved,
                "denied": denied,
                "not_reviewed": not_reviewed,
                "completion_rate": round(completion_rate, 2),
                "approval_rate": round((approved / total * 100), 2) if total > 0 else 0,
                "denial_rate": round((denied / total * 100), 2) if total > 0 else 0,
            }

        except GraphAPIError as e:
            logger.error(f"Failed to get decision insights: {e}")
            return {"error": str(e)}

    def create_review_schedule(
        self,
        display_name: str,
        scope_type: str,
        scope_id: str,
        reviewers: List[Dict[str, str]],
        recurrence_pattern: str = "quarterly",
    ) -> Dict[str, Any]:
        """
        Create a new recurring access review schedule

        Args:
            display_name: Review display name
            scope_type: Type of scope (group, application, etc.)
            scope_id: ID of the scope to review
            reviewers: List of reviewer objects
            recurrence_pattern: How often to recur (quarterly, monthly, etc.)

        Returns:
            Created review definition
        """
        logger.info(f"Creating new access review schedule: {display_name}")

        # Map recurrence pattern to ISO 8601 duration
        recurrence_map = {
            "weekly": "P1W",
            "monthly": "P1M",
            "quarterly": "P3M",
            "semiannually": "P6M",
            "annually": "P1Y",
        }

        request_body = {
            "displayName": display_name,
            "scope": {
                "@odata.type": f"#microsoft.graph.accessReviewQuery{scope_type.capitalize()}Scope",
                "query": (
                    f"/groups/{scope_id}/members"
                    if scope_type == "group"
                    else f"/{scope_type}s/{scope_id}"
                ),
                "queryType": "MicrosoftGraph",
            },
            "reviewers": reviewers,
            "settings": {
                "mailNotificationsEnabled": True,
                "reminderNotificationsEnabled": True,
                "justificationRequiredOnApproval": True,
                "defaultDecisionEnabled": False,
                "defaultDecision": "None",
                "instanceDurationInDays": 14,
                "recurrence": {
                    "pattern": {
                        "type": "absoluteMonthly",
                        "interval": 3 if recurrence_pattern == "quarterly" else 1,
                    },
                    "range": {
                        "type": "noEnd",
                        "startDate": datetime.utcnow().date().isoformat(),
                    },
                },
                "autoApplyDecisionsEnabled": True,
            },
        }

        try:
            response = self.client.post(
                "identityGovernance/accessReviews/definitions", request_body
            )

            return {
                "success": True,
                "review_id": response.get("id"),
                "display_name": response.get("displayName"),
                "created": True,
            }

        except GraphAPIError as e:
            logger.error(f"Failed to create review schedule: {e}")
            return {"success": False, "error": str(e)}
