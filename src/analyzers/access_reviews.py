"""
Access Reviews Analyzer
Analyzes and automates Entra ID Access Reviews for governance
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import Counter

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class AccessReviewAnalyzer:
    """
    Analyzes Access Review status and compliance
    """

    def __init__(self, use_beta: bool = True):
        """
        Initialize Access Review analyzer

        Args:
            use_beta: Use Graph API beta endpoint (required for Access Reviews)
        """
        self.client = GraphClient(use_beta=use_beta)

    def get_all_access_reviews(self) -> List[Dict[str, Any]]:
        """
        Get all access review schedule definitions

        Returns:
            List of access review definitions
        """
        try:
            logger.info("Fetching access review definitions")
            reviews = self.client.get_all_pages(
                "identityGovernance/accessReviews/definitions"
            )
            logger.info(f"Retrieved {len(reviews)} access review definitions")
            return reviews
        except GraphAPIError as e:
            logger.error(f"Failed to fetch access reviews: {e}")
            raise

    def get_review_instances(self, review_id: str) -> List[Dict[str, Any]]:
        """
        Get instances of a specific access review

        Args:
            review_id: Access review definition ID

        Returns:
            List of review instance objects
        """
        try:
            instances = self.client.get_all_pages(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances"
            )
            return instances
        except GraphAPIError as e:
            logger.error(f"Failed to fetch review instances: {e}")
            return []

    def get_review_decisions(self, review_id: str, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get decisions for a specific review instance

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID

        Returns:
            List of decision objects
        """
        try:
            decisions = self.client.get_all_pages(
                f"identityGovernance/accessReviews/definitions/{review_id}/instances/{instance_id}/decisions"
            )
            return decisions
        except GraphAPIError as e:
            logger.error(f"Failed to fetch review decisions: {e}")
            return []

    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        """
        Get all pending access reviews that need attention

        Returns:
            List of pending review instances
        """
        reviews = self.get_all_access_reviews()
        pending = []

        for review in reviews:
            if review.get("status") != "Completed":
                instances = self.get_review_instances(review["id"])

                for instance in instances:
                    if instance.get("status") == "InProgress":
                        # Get decisions to check completion
                        decisions = self.get_review_decisions(review["id"], instance["id"])

                        pending_decisions = sum(
                            1 for d in decisions
                            if d.get("decision") == "NotReviewed"
                        )

                        if pending_decisions > 0:
                            pending.append({
                                "review_id": review["id"],
                                "review_name": review.get("displayName"),
                                "instance_id": instance["id"],
                                "status": instance.get("status"),
                                "start_date": instance.get("startDateTime"),
                                "end_date": instance.get("endDateTime"),
                                "pending_decisions": pending_decisions,
                                "total_decisions": len(decisions)
                            })

        logger.info(f"Found {len(pending)} pending review instances")
        return pending

    def analyze_review_completion_rate(self) -> Dict[str, Any]:
        """
        Analyze completion rates for access reviews

        Returns:
            Completion rate analysis
        """
        reviews = self.get_all_access_reviews()

        total_reviews = 0
        completed_reviews = 0
        in_progress = 0
        not_started = 0

        review_details = []

        for review in reviews:
            instances = self.get_review_instances(review["id"])

            for instance in instances:
                total_reviews += 1
                status = instance.get("status")

                if status == "Completed":
                    completed_reviews += 1
                elif status == "InProgress":
                    in_progress += 1
                else:
                    not_started += 1

                # Get completion percentage for this instance
                decisions = self.get_review_decisions(review["id"], instance["id"])
                total_decisions = len(decisions)
                completed_decisions = sum(
                    1 for d in decisions
                    if d.get("decision") != "NotReviewed"
                )

                completion_pct = (completed_decisions / total_decisions * 100) if total_decisions > 0 else 0

                review_details.append({
                    "review_name": review.get("displayName"),
                    "instance_id": instance["id"],
                    "status": status,
                    "completion_percentage": round(completion_pct, 2),
                    "completed_decisions": completed_decisions,
                    "total_decisions": total_decisions
                })

        overall_completion = (completed_reviews / total_reviews * 100) if total_reviews > 0 else 0

        return {
            "summary": {
                "total_review_instances": total_reviews,
                "completed": completed_reviews,
                "in_progress": in_progress,
                "not_started": not_started,
                "overall_completion_rate": round(overall_completion, 2)
            },
            "reviews": review_details,
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_overdue_reviews(self) -> List[Dict[str, Any]]:
        """
        Find access reviews that are past their due date

        Returns:
            List of overdue reviews
        """
        reviews = self.get_all_access_reviews()
        overdue = []
        current_time = datetime.utcnow()

        for review in reviews:
            instances = self.get_review_instances(review["id"])

            for instance in instances:
                end_date_str = instance.get("endDateTime")
                if not end_date_str:
                    continue

                try:
                    end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                    end_date_naive = end_date.replace(tzinfo=None)

                    if end_date_naive < current_time and instance.get("status") != "Completed":
                        # Get pending decisions
                        decisions = self.get_review_decisions(review["id"], instance["id"])
                        pending_count = sum(
                            1 for d in decisions
                            if d.get("decision") == "NotReviewed"
                        )

                        days_overdue = (current_time - end_date_naive).days

                        overdue.append({
                            "review_id": review["id"],
                            "review_name": review.get("displayName"),
                            "instance_id": instance["id"],
                            "end_date": end_date_str,
                            "days_overdue": days_overdue,
                            "pending_decisions": pending_count,
                            "severity": "HIGH" if days_overdue > 7 else "MEDIUM"
                        })
                except Exception as e:
                    logger.warning(f"Error parsing date for review {review.get('id')}: {e}")

        overdue.sort(key=lambda x: x["days_overdue"], reverse=True)
        logger.info(f"Found {len(overdue)} overdue reviews")
        return overdue

    def analyze_reviewer_performance(self) -> Dict[str, Any]:
        """
        Analyze reviewer response rates and performance

        Returns:
            Reviewer performance analysis
        """
        reviews = self.get_all_access_reviews()

        reviewer_stats = Counter()
        reviewer_completed = Counter()

        for review in reviews:
            instances = self.get_review_instances(review["id"])

            for instance in instances:
                decisions = self.get_review_decisions(review["id"], instance["id"])

                for decision in decisions:
                    reviewer_id = decision.get("reviewedBy", {}).get("id")
                    if reviewer_id:
                        reviewer_stats[reviewer_id] += 1

                        if decision.get("decision") != "NotReviewed":
                            reviewer_completed[reviewer_id] += 1

        # Calculate completion rates
        reviewer_performance = []
        for reviewer_id, total in reviewer_stats.items():
            completed = reviewer_completed.get(reviewer_id, 0)
            completion_rate = (completed / total * 100) if total > 0 else 0

            reviewer_performance.append({
                "reviewer_id": reviewer_id,
                "total_reviews_assigned": total,
                "completed_reviews": completed,
                "completion_rate": round(completion_rate, 2),
                "performance_rating": "Good" if completion_rate >= 80 else "Needs Improvement"
            })

        reviewer_performance.sort(key=lambda x: x["completion_rate"], reverse=True)

        return {
            "total_reviewers": len(reviewer_stats),
            "average_completion_rate": round(
                sum(r["completion_rate"] for r in reviewer_performance) / len(reviewer_performance), 2
            ) if reviewer_performance else 0,
            "reviewers": reviewer_performance,
            "timestamp": datetime.utcnow().isoformat()
        }

    def generate_review_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive access review governance report

        Returns:
            Complete governance report
        """
        logger.info("Generating comprehensive access review report")

        completion_analysis = self.analyze_review_completion_rate()
        pending_reviews = self.get_pending_reviews()
        overdue_reviews = self.get_overdue_reviews()

        # Generate recommendations
        recommendations = []

        if completion_analysis["summary"]["overall_completion_rate"] < 80:
            recommendations.append(
                "LOW completion rate detected. Send reminders to reviewers and consider escalation process."
            )

        if len(overdue_reviews) > 0:
            recommendations.append(
                f"{len(overdue_reviews)} reviews are overdue. Immediate action required."
            )

        if len(pending_reviews) > 5:
            recommendations.append(
                f"{len(pending_reviews)} reviews pending. Consider automated reminders."
            )

        return {
            "summary": {
                "total_reviews": completion_analysis["summary"]["total_review_instances"],
                "completion_rate": completion_analysis["summary"]["overall_completion_rate"],
                "pending_reviews": len(pending_reviews),
                "overdue_reviews": len(overdue_reviews)
            },
            "completion_analysis": completion_analysis,
            "pending_reviews": pending_reviews[:10],  # Top 10
            "overdue_reviews": overdue_reviews[:10],  # Top 10
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }

    def send_reviewer_reminder(self, review_id: str, instance_id: str, reviewer_id: str) -> bool:
        """
        Send reminder to reviewer (placeholder for email/notification integration)

        Args:
            review_id: Access review definition ID
            instance_id: Review instance ID
            reviewer_id: Reviewer user ID

        Returns:
            True if reminder sent successfully
        """
        # This is a placeholder - in production, integrate with email service
        logger.info(f"Reminder would be sent to reviewer {reviewer_id} for review {review_id}/{instance_id}")

        # Could integrate with:
        # - Microsoft Graph sendMail API
        # - Teams notifications
        # - ServiceNow tickets
        # - Custom notification service

        return True

    def auto_remind_pending_reviewers(self, days_before_due: int = 3) -> int:
        """
        Automatically remind reviewers of pending reviews

        Args:
            days_before_due: Send reminder if review due within N days

        Returns:
            Number of reminders sent
        """
        pending = self.get_pending_reviews()
        reminders_sent = 0
        current_time = datetime.utcnow()

        for review in pending:
            end_date_str = review.get("end_date")
            if not end_date_str:
                continue

            try:
                end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                end_date_naive = end_date.replace(tzinfo=None)
                days_until_due = (end_date_naive - current_time).days

                if 0 <= days_until_due <= days_before_due:
                    # Get reviewers with pending decisions
                    decisions = self.get_review_decisions(
                        review["review_id"],
                        review["instance_id"]
                    )

                    for decision in decisions:
                        if decision.get("decision") == "NotReviewed":
                            reviewer_id = decision.get("reviewedBy", {}).get("id")
                            if reviewer_id:
                                self.send_reviewer_reminder(
                                    review["review_id"],
                                    review["instance_id"],
                                    reviewer_id
                                )
                                reminders_sent += 1

            except Exception as e:
                logger.warning(f"Error processing reminder for review {review.get('review_id')}: {e}")

        logger.info(f"Sent {reminders_sent} reviewer reminders")
        return reminders_sent
