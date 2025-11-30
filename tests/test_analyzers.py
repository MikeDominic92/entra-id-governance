"""
Tests for Analyzers
"""

import pytest
from unittest.mock import Mock, patch
from src.analyzers import ConditionalAccessAnalyzer, PIMAnalyzer


class TestConditionalAccessAnalyzer:
    """Test suite for ConditionalAccessAnalyzer"""

    @patch('src.analyzers.conditional_access.GraphClient')
    def test_policy_score_calculation(self, mock_client):
        """Test policy scoring"""
        from src.analyzers.conditional_access import PolicyScore

        # Policy with MFA
        policy_with_mfa = {
            "grantControls": {
                "builtInControls": ["mfa"]
            },
            "conditions": {
                "clientAppTypes": []
            }
        }

        score = PolicyScore.calculate_policy_score(policy_with_mfa)
        assert score >= 25  # MFA weight

        # Policy with device compliance
        policy_with_device = {
            "grantControls": {
                "builtInControls": ["compliantDevice"]
            },
            "conditions": {
                "clientAppTypes": []
            }
        }

        score = PolicyScore.calculate_policy_score(policy_with_device)
        assert score >= 20  # Device compliance weight

    @patch('src.analyzers.conditional_access.GraphClient')
    def test_coverage_analysis(self, mock_client):
        """Test policy coverage analysis"""
        mock_graph = Mock()
        mock_graph.get_all_pages.return_value = [
            {
                "id": "1",
                "displayName": "Test Policy",
                "state": "enabled",
                "conditions": {
                    "users": {"includeUsers": ["All"]},
                    "applications": {"includeApplications": ["All"]},
                    "clientAppTypes": []
                },
                "grantControls": {"builtInControls": ["mfa"]}
            }
        ]
        mock_client.return_value = mock_graph

        analyzer = ConditionalAccessAnalyzer()
        coverage = analyzer.analyze_policy_coverage()

        assert "summary" in coverage
        assert coverage["summary"]["total_policies"] == 1
        assert coverage["summary"]["enabled"] == 1

    @patch('src.analyzers.conditional_access.GraphClient')
    def test_recommendations(self, mock_client):
        """Test recommendation generation"""
        mock_graph = Mock()
        # No policies scenario
        mock_graph.get_all_pages.return_value = []
        mock_client.return_value = mock_graph

        analyzer = ConditionalAccessAnalyzer()
        recommendations = analyzer.generate_recommendations()

        assert len(recommendations) > 0
        assert any("MFA" in rec for rec in recommendations)


class TestPIMAnalyzer:
    """Test suite for PIMAnalyzer"""

    @patch('src.analyzers.pim_analyzer.GraphClient')
    def test_standing_access_detection(self, mock_client):
        """Test detection of standing admin access"""
        mock_graph = Mock()

        # Mock role definitions
        mock_graph.get_all_pages.side_effect = [
            # First call: role definitions
            [
                {"id": "role1", "displayName": "Global Administrator"}
            ],
            # Second call: active assignments (if called)
            []
        ]

        mock_client.return_value = mock_graph

        analyzer = PIMAnalyzer()

        # Test with standing access
        active_assignments = [
            {
                "id": "assign1",
                "principalId": "user1",
                "roleDefinitionId": "role1",
                "endDateTime": None  # No end date = permanent
            }
        ]

        violations = analyzer.detect_standing_admin_access(active_assignments)

        assert len(violations) > 0
        assert violations[0]["severity"] == "HIGH"

    @patch('src.analyzers.pim_analyzer.GraphClient')
    def test_excessive_assignments(self, mock_client):
        """Test detection of excessive role assignments"""
        mock_graph = Mock()

        # Mock role definitions
        mock_graph.get_all_pages.side_effect = [
            [
                {"id": "role1", "displayName": "Role 1"},
                {"id": "role2", "displayName": "Role 2"},
                {"id": "role3", "displayName": "Role 3"}
            ]
        ]

        mock_client.return_value = mock_graph

        analyzer = PIMAnalyzer()

        # User with many roles
        eligible_assignments = [
            {
                "principalId": "user1",
                "roleDefinitionId": "role1"
            },
            {
                "principalId": "user1",
                "roleDefinitionId": "role2"
            },
            {
                "principalId": "user1",
                "roleDefinitionId": "role3"
            }
        ]

        excessive = analyzer.check_excessive_role_assignments(
            eligible_assignments,
            threshold=2
        )

        assert len(excessive) > 0
        assert excessive[0]["principal_id"] == "user1"
        assert excessive[0]["role_count"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
