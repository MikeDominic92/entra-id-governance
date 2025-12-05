# ISO 27001:2022 Annex A Control Mapping

> **Chainguard Relevance:** This document demonstrates expertise in "SOC 2, ISO 27001, and other regulatory audits" - a key requirement for IT Engineer (Identity/IAM) roles.

## Overview

This document maps Entra ID Governance Toolkit capabilities to ISO 27001:2022 Annex A controls, focusing on identity and access management requirements.

**Standard Version:** ISO/IEC 27001:2022
**Prepared By:** Mike Dominic
**Last Updated:** December 2025

---

## Annex A Control Coverage

| Domain | Controls Applicable | Fully Implemented | Partially Implemented |
|--------|---------------------|-------------------|----------------------|
| A.5 - Organizational | 4 | 4 | 0 |
| A.6 - People | 2 | 2 | 0 |
| A.7 - Physical | 0 | N/A | N/A |
| A.8 - Technological | 12 | 12 | 0 |
| **Total** | **18** | **18** | **0** |

---

## A.5 - Organizational Controls

### A.5.15 - Access Control

**Control:** Rules to control physical and logical access to information and other associated assets shall be established and implemented based on business and information security requirements.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Annual |

**Implementation Evidence:**

1. **Conditional Access Policies**
   - 45 active policies covering all access scenarios
   - Role-based access control (RBAC) implementation
   - Location and device-based restrictions

2. **Policy Documentation**
   - Access control policy (DOC-IAM-001)
   - Conditional access standards (DOC-IAM-002)
   - Exception handling procedures (DOC-IAM-003)

**Toolkit Features:**
```python
# Analyze access control policy coverage
from src.analyzers import ConditionalAccessAnalyzer

analyzer = ConditionalAccessAnalyzer()
coverage = analyzer.get_policy_coverage()

# Returns: {
#   "total_policies": 45,
#   "coverage_percentage": 98.5,
#   "gaps": ["guest_users_without_mfa"]
# }
```

---

### A.5.16 - Identity Management

**Control:** The full lifecycle of identities shall be managed.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

1. **Lifecycle Automation**
   - Joiner/Mover/Leaver workflows integrated with HRIS
   - Automated deprovisioning within 24 hours
   - Identity correlation across systems

2. **Identity Governance**
   - Unique identity per user
   - Service account management
   - Guest identity lifecycle

**Toolkit Features:**
```python
# Track identity lifecycle metrics
from src.governance import IdentityLifecycleTracker

tracker = IdentityLifecycleTracker()
metrics = tracker.get_lifecycle_metrics()

# Returns: {
#   "avg_provisioning_time_hours": 2.3,
#   "avg_deprovisioning_time_hours": 4.1,
#   "orphaned_accounts": 0,
#   "stale_accounts_90d": 12
# }
```

---

### A.5.17 - Authentication Information

**Control:** Allocation and management of authentication information shall be controlled by a management process.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

1. **MFA Enforcement**
   - 99.2% of users with MFA enrolled
   - Passwordless authentication available
   - FIDO2 security keys supported

2. **Authentication Methods**
   - Microsoft Authenticator (primary)
   - FIDO2 security keys
   - SMS/Voice (legacy, being deprecated)

**Toolkit Features:**
```python
# Analyze authentication method coverage
from src.analyzers import AuthenticationAnalyzer

analyzer = AuthenticationAnalyzer()
mfa_report = analyzer.get_mfa_coverage()

# Returns: {
#   "mfa_enrolled_percentage": 99.2,
#   "passwordless_percentage": 45.3,
#   "legacy_methods_users": 23
# }
```

---

### A.5.18 - Access Rights

**Control:** Access rights to information and other associated assets shall be provisioned, reviewed, modified and removed in accordance with the organization's topic-specific policy.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Quarterly |

**Implementation Evidence:**

1. **Access Provisioning**
   - RBAC-based provisioning
   - Manager approval workflow
   - Justification required

2. **Access Reviews**
   - Quarterly certification campaigns
   - Manager-based reviews
   - Automated reminders and escalation

3. **Access Revocation**
   - Automated on termination
   - Manual revocation workflow
   - Emergency access removal (<1 hour SLA)

**Toolkit Features:**
```python
# Generate access review report
from src.governance import AccessReviewManager

manager = AccessReviewManager()
review = manager.get_quarterly_review_status("Q4-2025")

# Returns: {
#   "total_reviews": 1250,
#   "completed": 1245,
#   "completion_rate": 99.6,
#   "access_revoked": 47
# }
```

---

## A.6 - People Controls

### A.6.1 - Screening

**Control:** Background verification checks on all candidates shall be carried out.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | HR + IAM Team |
| **Review Frequency** | Per-hire |

**Implementation Evidence:**

- Pre-employment screening integrated with HRIS
- Access provisioned only after screening complete
- Contractor screening requirements enforced

---

### A.6.5 - Responsibilities After Termination

**Control:** Information security responsibilities that remain valid after termination shall be defined, enforced and communicated.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Per-termination |

**Implementation Evidence:**

- Immediate access revocation on termination
- Compliance hold for audit requirements
- Exit interview acknowledgment

---

## A.8 - Technological Controls

### A.8.2 - Privileged Access Rights

**Control:** The allocation and use of privileged access rights shall be restricted and managed.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

1. **PIM Implementation**
   - Just-in-time access for all admin roles
   - Maximum activation duration: 8 hours
   - MFA required for activation
   - Justification required

2. **Standing Admin Policy**
   - Zero standing admins (except break-glass)
   - Monthly standing admin audits
   - Automatic detection and alerting

**Toolkit Features:**
```python
# Monitor privileged access
from src.analyzers import PIMAnalyzer

analyzer = PIMAnalyzer()
pim_status = analyzer.get_compliance_status()

# Returns: {
#   "standing_admins": 2,  # Break-glass only
#   "pim_managed_roles": 28,
#   "avg_activation_duration_hours": 2.3,
#   "activations_last_30d": 245
# }
```

---

### A.8.3 - Information Access Restriction

**Control:** Access to information and other associated assets shall be restricted in accordance with the established topic-specific policy.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

- Conditional Access enforcement
- Data Loss Prevention integration
- Sensitivity label access controls

---

### A.8.5 - Secure Authentication

**Control:** Secure authentication technologies and procedures shall be implemented.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Review Frequency** | Annual |

**Implementation Evidence:**

1. **Authentication Security**
   - Modern authentication enforced
   - Legacy authentication blocked
   - Token lifetime restrictions

2. **Session Management**
   - Conditional Access session controls
   - Sign-in risk policies
   - Continuous access evaluation

---

### A.8.15 - Logging

**Control:** Logs that record activities, exceptions, faults and other relevant events shall be produced, stored, protected and analyzed.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

1. **Log Collection**
   - Microsoft Graph API audit logs
   - Sign-in logs
   - PIM activation logs
   - Conditional Access logs

2. **Log Analysis**
   - Splunk SIEM integration
   - Real-time alerting
   - Anomaly detection

**Toolkit Features:**
```python
# Forward events to SIEM
from src.integrations import SplunkIntegration

splunk = SplunkIntegration(
    hec_url="https://splunk.example.com:8088",
    token="your-hec-token"
)

# Forward all identity events
splunk.forward_events(event_types=["sign_in", "pim", "ca_policy"])
```

---

### A.8.16 - Monitoring Activities

**Control:** Networks, systems and applications shall be monitored for anomalous behavior.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Review Frequency** | Continuous |

**Implementation Evidence:**

1. **Identity Monitoring**
   - Risk-based sign-in detection
   - Impossible travel detection
   - Unfamiliar location alerts

2. **Behavior Analytics**
   - User and Entity Behavior Analytics (UEBA)
   - Baseline deviation detection
   - Insider threat indicators

---

### A.8.18 - Use of Privileged Utility Programs

**Control:** The use of utility programs that might be capable of overriding system controls shall be restricted and tightly controlled.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Review Frequency** | Monthly |

**Implementation Evidence:**

- Admin tool access via PIM only
- PowerShell/Graph API access logged
- Sensitive operations require approval

---

## Audit Evidence Package

### Evidence Types by Control

| Control | Evidence Type | Location | Format |
|---------|--------------|----------|--------|
| A.5.15 | CA Policy Report | `/evidence/a5-15/` | JSON, PDF |
| A.5.16 | Lifecycle Metrics | `/evidence/a5-16/` | JSON, PDF |
| A.5.17 | MFA Coverage | `/evidence/a5-17/` | JSON, PDF |
| A.5.18 | Access Reviews | `/evidence/a5-18/` | JSON, PDF |
| A.8.2 | PIM Compliance | `/evidence/a8-2/` | JSON, PDF |
| A.8.15 | Log Samples | `/evidence/a8-15/` | JSON |
| A.8.16 | Alert Reports | `/evidence/a8-16/` | JSON, PDF |

### Generate ISO 27001 Evidence Package

```python
from src.compliance import generate_iso27001_evidence_package

package = generate_iso27001_evidence_package(
    audit_period="2025",
    controls=["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.2"],
    output_path="/audit-evidence/iso27001-2025/"
)
```

---

## Statement of Applicability (SoA) Excerpt

| Control | Applicable | Implemented | Justification |
|---------|------------|-------------|---------------|
| A.5.15 | Yes | Yes | Access control for cloud identity |
| A.5.16 | Yes | Yes | Full identity lifecycle management |
| A.5.17 | Yes | Yes | MFA and authentication management |
| A.5.18 | Yes | Yes | Quarterly access reviews |
| A.8.2 | Yes | Yes | PIM for privileged access |
| A.8.3 | Yes | Yes | Conditional Access enforcement |
| A.8.5 | Yes | Yes | Modern authentication |
| A.8.15 | Yes | Yes | Comprehensive logging |
| A.8.16 | Yes | Yes | SIEM-based monitoring |

---

## Certification Readiness

### Pre-Audit Checklist

- [x] All applicable controls documented
- [x] Evidence collection automated
- [x] Control owners assigned
- [x] Testing completed within 12 months
- [x] Gap remediation complete
- [x] Management attestation obtained

### Internal Audit Results

| Audit Date | Auditor | Non-Conformities | Observations |
|------------|---------|------------------|--------------|
| 2025-06-15 | Internal | 0 | 2 minor |
| 2025-09-20 | Internal | 0 | 1 minor |

---

*This document supports ISO 27001:2022 certification audit evidence requirements.*
*Prepared for Chainguard IT Engineer (Identity/IAM) Portfolio - Mike Dominic*
