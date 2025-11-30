"""
Analyzers for Entra ID Governance
"""

from .conditional_access import ConditionalAccessAnalyzer
from .pim_analyzer import PIMAnalyzer
from .access_reviews import AccessReviewAnalyzer
from .entitlements import EntitlementAnalyzer

__all__ = [
    "ConditionalAccessAnalyzer",
    "PIMAnalyzer",
    "AccessReviewAnalyzer",
    "EntitlementAnalyzer",
]
