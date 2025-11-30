"""
Entitlement Management Analyzer
Analyzes access packages, catalogs, and entitlement policies
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter

from ..graph_client import GraphClient, GraphAPIError

logger = logging.getLogger(__name__)


class EntitlementAnalyzer:
    """
    Analyzes Entitlement Management for governance
    """

    def __init__(self, use_beta: bool = True):
        """
        Initialize Entitlement analyzer

        Args:
            use_beta: Use Graph API beta endpoint
        """
        self.client = GraphClient(use_beta=use_beta)

    def get_access_packages(self) -> List[Dict[str, Any]]:
        """
        Get all access packages

        Returns:
            List of access package objects
        """
        try:
            logger.info("Fetching access packages")
            packages = self.client.get_all_pages(
                "identityGovernance/entitlementManagement/accessPackages"
            )
            logger.info(f"Retrieved {len(packages)} access packages")
            return packages
        except GraphAPIError as e:
            logger.error(f"Failed to fetch access packages: {e}")
            raise

    def get_catalogs(self) -> List[Dict[str, Any]]:
        """
        Get all access package catalogs

        Returns:
            List of catalog objects
        """
        try:
            logger.info("Fetching catalogs")
            catalogs = self.client.get_all_pages(
                "identityGovernance/entitlementManagement/catalogs"
            )
            logger.info(f"Retrieved {len(catalogs)} catalogs")
            return catalogs
        except GraphAPIError as e:
            logger.error(f"Failed to fetch catalogs: {e}")
            raise

    def get_assignment_policies(self, package_id: str) -> List[Dict[str, Any]]:
        """
        Get assignment policies for an access package

        Args:
            package_id: Access package ID

        Returns:
            List of policy objects
        """
        try:
            policies = self.client.get_all_pages(
                f"identityGovernance/entitlementManagement/accessPackages/{package_id}/assignmentPolicies"
            )
            return policies
        except GraphAPIError as e:
            logger.error(f"Failed to fetch assignment policies: {e}")
            return []

    def get_assignments(self, package_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get access package assignments

        Args:
            package_id: Optional package ID to filter by

        Returns:
            List of assignment objects
        """
        try:
            endpoint = "identityGovernance/entitlementManagement/assignments"

            if package_id:
                assignments = self.client.get_all_pages(
                    endpoint, params={"$filter": f"accessPackage/id eq '{package_id}'"}
                )
            else:
                assignments = self.client.get_all_pages(endpoint)

            logger.info(f"Retrieved {len(assignments)} assignments")
            return assignments
        except GraphAPIError as e:
            logger.error(f"Failed to fetch assignments: {e}")
            return []

    def analyze_access_packages(self) -> Dict[str, Any]:
        """
        Analyze access package configuration and usage

        Returns:
            Analysis report
        """
        packages = self.get_access_packages()
        catalogs = self.get_catalogs()

        catalog_map = {c["id"]: c["displayName"] for c in catalogs}

        package_details = []
        total_assignments = 0

        for package in packages:
            package_id = package["id"]
            catalog_id = package.get("catalogId")

            # Get policies
            policies = self.get_assignment_policies(package_id)

            # Get assignments
            assignments = self.get_assignments(package_id)
            assignment_count = len(assignments)
            total_assignments += assignment_count

            # Analyze policies
            has_approval = any(
                policy.get("requestApprovalSettings", {}).get(
                    "isApprovalRequired", False
                )
                for policy in policies
            )

            has_expiration = any(
                policy.get("requestorSettings", {})
                .get("expirationSettings", {})
                .get("expirationDuration")
                for policy in policies
            )

            package_details.append(
                {
                    "id": package_id,
                    "displayName": package.get("displayName"),
                    "catalog": catalog_map.get(catalog_id, "Unknown"),
                    "is_hidden": package.get("isHidden", False),
                    "state": package.get("state"),
                    "policy_count": len(policies),
                    "assignment_count": assignment_count,
                    "requires_approval": has_approval,
                    "has_expiration": has_expiration,
                }
            )

        return {
            "summary": {
                "total_packages": len(packages),
                "total_catalogs": len(catalogs),
                "total_assignments": total_assignments,
                "average_assignments_per_package": (
                    round(total_assignments / len(packages), 2) if packages else 0
                ),
            },
            "packages": package_details,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def detect_overprivileged_packages(self) -> List[Dict[str, Any]]:
        """
        Detect access packages that may grant excessive permissions

        Returns:
            List of potentially overprivileged packages
        """
        packages = self.get_access_packages()
        overprivileged = []

        for package in packages:
            package_id = package["id"]
            policies = self.get_assignment_policies(package_id)

            # Check for packages without approval requirements
            requires_approval = any(
                policy.get("requestApprovalSettings", {}).get(
                    "isApprovalRequired", False
                )
                for policy in policies
            )

            # Check for packages without expiration
            has_expiration = any(
                policy.get("requestorSettings", {})
                .get("expirationSettings", {})
                .get("expirationDuration")
                for policy in policies
            )

            # Get assignments to see usage
            assignments = self.get_assignments(package_id)

            # Flag packages with high usage but no governance controls
            if len(assignments) > 10 and (not requires_approval or not has_expiration):
                overprivileged.append(
                    {
                        "package_id": package_id,
                        "displayName": package.get("displayName"),
                        "assignment_count": len(assignments),
                        "requires_approval": requires_approval,
                        "has_expiration": has_expiration,
                        "risk_level": (
                            "HIGH"
                            if not requires_approval and not has_expiration
                            else "MEDIUM"
                        ),
                        "recommendation": "Add approval workflow and expiration policy for high-usage packages",
                    }
                )

        overprivileged.sort(key=lambda x: x["assignment_count"], reverse=True)
        logger.info(
            f"Detected {len(overprivileged)} potentially overprivileged packages"
        )

        return overprivileged

    def analyze_catalog_governance(self) -> Dict[str, Any]:
        """
        Analyze catalog governance and organization

        Returns:
            Catalog governance report
        """
        catalogs = self.get_catalogs()
        packages = self.get_access_packages()

        # Count packages per catalog
        packages_per_catalog = Counter()
        for package in packages:
            catalog_id = package.get("catalogId")
            if catalog_id:
                packages_per_catalog[catalog_id] += 1

        catalog_details = []
        for catalog in catalogs:
            catalog_id = catalog["id"]
            package_count = packages_per_catalog.get(catalog_id, 0)

            catalog_details.append(
                {
                    "id": catalog_id,
                    "displayName": catalog.get("displayName"),
                    "description": catalog.get("description"),
                    "catalogType": catalog.get("catalogType"),
                    "state": catalog.get("state"),
                    "isExternallyVisible": catalog.get("isExternallyVisible", False),
                    "package_count": package_count,
                }
            )

        # Identify empty catalogs
        empty_catalogs = [c for c in catalog_details if c["package_count"] == 0]

        return {
            "summary": {
                "total_catalogs": len(catalogs),
                "empty_catalogs": len(empty_catalogs),
                "average_packages_per_catalog": (
                    round(sum(packages_per_catalog.values()) / len(catalogs), 2)
                    if catalogs
                    else 0
                ),
            },
            "catalogs": catalog_details,
            "recommendations": [
                (
                    f"Remove {len(empty_catalogs)} empty catalogs"
                    if empty_catalogs
                    else "Catalog organization is good"
                ),
                "Consider consolidating catalogs with similar purposes",
                "Ensure catalog names clearly indicate their purpose",
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_expiring_assignments(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get assignments expiring within N days

        Args:
            days: Number of days to look ahead

        Returns:
            List of expiring assignments
        """
        assignments = self.get_assignments()
        expiring = []
        current_time = datetime.utcnow()

        for assignment in assignments:
            schedule = assignment.get("schedule", {})
            expiration = schedule.get("expiration", {})
            end_date_str = expiration.get("endDateTime")

            if end_date_str:
                try:
                    end_date = datetime.fromisoformat(
                        end_date_str.replace("Z", "+00:00")
                    )
                    end_date_naive = end_date.replace(tzinfo=None)
                    days_until_expiration = (end_date_naive - current_time).days

                    if 0 <= days_until_expiration <= days:
                        expiring.append(
                            {
                                "assignment_id": assignment.get("id"),
                                "target_id": assignment.get("target", {}).get("id"),
                                "access_package_id": assignment.get("accessPackageId"),
                                "expiration_date": end_date_str,
                                "days_until_expiration": days_until_expiration,
                                "state": assignment.get("state"),
                            }
                        )
                except Exception as e:
                    logger.warning(f"Error parsing expiration date: {e}")

        expiring.sort(key=lambda x: x["days_until_expiration"])
        logger.info(f"Found {len(expiring)} assignments expiring within {days} days")

        return expiring

    def generate_entitlement_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive entitlement management report

        Returns:
            Complete entitlement governance report
        """
        logger.info("Generating comprehensive entitlement management report")

        package_analysis = self.analyze_access_packages()
        catalog_analysis = self.analyze_catalog_governance()
        overprivileged = self.detect_overprivileged_packages()
        expiring = self.get_expiring_assignments(30)

        # Generate recommendations
        recommendations = []

        if len(overprivileged) > 0:
            recommendations.append(
                f"HIGH: {len(overprivileged)} access packages lack proper governance controls. "
                "Add approval workflows and expiration policies."
            )

        if catalog_analysis["summary"]["empty_catalogs"] > 0:
            recommendations.append(
                f"MEDIUM: {catalog_analysis['summary']['empty_catalogs']} empty catalogs should be removed."
            )

        if len(expiring) > 0:
            recommendations.append(
                f"INFO: {len(expiring)} assignments expiring in next 30 days. "
                "Notify users to renew if needed."
            )

        recommendations.extend(
            [
                "INFO: Regularly review access package assignments for compliance",
                "INFO: Use connected organizations for external user management",
                "INFO: Enable access reviews for long-term assignments",
            ]
        )

        return {
            "summary": {
                "total_packages": package_analysis["summary"]["total_packages"],
                "total_catalogs": catalog_analysis["summary"]["total_catalogs"],
                "total_assignments": package_analysis["summary"]["total_assignments"],
                "overprivileged_packages": len(overprivileged),
                "expiring_assignments": len(expiring),
            },
            "package_analysis": package_analysis,
            "catalog_analysis": catalog_analysis,
            "overprivileged_packages": overprivileged[:10],
            "expiring_assignments": expiring[:10],
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat(),
        }
