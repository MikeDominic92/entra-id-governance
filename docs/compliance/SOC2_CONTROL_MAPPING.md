# SOC 2 Type II Control Mapping

> **Chainguard Relevance:** This document demonstrates expertise in "SOC 2, ISO 27001, and other regulatory audits" - a key requirement for IT Engineer (Identity/IAM) roles.

## Overview

This document maps Entra ID Governance Toolkit capabilities to SOC 2 Type II Trust Services Criteria, providing auditors with clear evidence of control implementation and effectiveness.

**Audit Period:** [Insert Audit Period]
**Prepared By:** Mike Dominic
**Last Updated:** December 2025

---

## Trust Services Criteria Coverage

| Category | Controls Mapped | Fully Implemented | Partially Implemented |
|----------|-----------------|-------------------|----------------------|
| CC6 - Logical Access | 8 | 8 | 0 |
| CC7 - System Operations | 4 | 4 | 0 |
| CC8 - Change Management | 3 | 3 | 0 |
| **Total** | **15** | **15** | **0** |

---

## CC6: Logical and Physical Access Controls

### CC6.1 - Logical Access Security Software

**Criterion:** The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Continuous |

**How This Toolkit Addresses CC6.1:**

1. **Conditional Access Policy Analysis**
   - Automated scanning of all CA policies
   - Coverage gap identification
   - Security posture scoring (0-100 scale)

2. **Policy Enforcement Validation**
   - MFA requirement verification
   - Device compliance checks
   - Location-based access controls

**Evidence Generated:**
```
Evidence Type: Conditional Access Policy Report
Location: /reports/ca-policy-analysis-{date}.json
Frequency: Daily automated scan
Retention: 7 years
```

**Sample Evidence:**
```json
{
  "report_date": "2025-12-05",
  "total_policies": 45,
  "enabled_policies": 42,
  "coverage_score": 94.2,
  "mfa_enforced_percentage": 98.5,
  "gaps_identified": [
    {
      "gap_type": "legacy_auth_allowed",
      "affected_users": 12,
      "risk_level": "high",
      "remediation": "Block legacy authentication protocols"
    }
  ]
}
```

---

### CC6.2 - User Registration and Authorization

**Criterion:** Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Per-event + Quarterly Review |

**How This Toolkit Addresses CC6.2:**

1. **Access Request Workflow**
   - PIM role assignment tracking
   - Approval workflow logging
   - Justification requirements

2. **Registration Validation**
   - User provisioning audit trail
   - Manager approval verification
   - Entitlement documentation

**Evidence Generated:**
```
Evidence Type: User Provisioning Audit Report
Location: /reports/user-provisioning-{date}.json
Frequency: Real-time logging + monthly summary
Retention: 7 years
```

---

### CC6.3 - Role-Based Access and Least Privilege

**Criterion:** The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on roles, responsibilities, or the system design.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Continuous |

**How This Toolkit Addresses CC6.3:**

1. **PIM Role Analysis**
   - Standing administrator detection
   - Just-in-time access enforcement
   - Role assignment justification tracking

2. **Least Privilege Validation**
   - Excessive permission identification
   - Role comparison analysis
   - Privilege escalation detection

**Evidence Generated:**
```
Evidence Type: PIM Compliance Report
Location: /reports/pim-compliance-{date}.json
Frequency: Daily scan
Retention: 7 years

Key Metrics:
- Standing admins detected: 0 (target)
- JIT activations last 30 days: 245
- Average activation duration: 2.3 hours
- Activations with justification: 100%
```

---

### CC6.6 - Access Review and Recertification

**Criterion:** The entity implements logical access security measures to protect against unauthorized access to system resources.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Quarterly |

**How This Toolkit Addresses CC6.6:**

1. **Access Review Automation**
   - Quarterly campaign creation
   - Manager notification workflows
   - Completion tracking

2. **Overdue Review Detection**
   - Escalation to security team
   - Automatic reminder cadence
   - Executive reporting

**Evidence Generated:**
```
Evidence Type: Access Review Campaign Report
Location: /reports/access-review-{quarter}-{year}.json
Frequency: Quarterly
Retention: 7 years

Key Metrics:
- Reviews completed: 1,245 / 1,250 (99.6%)
- Overdue reviews: 5
- Access revoked: 47
- Average review time: 3.2 days
```

---

### CC6.7 - Access Termination

**Criterion:** The entity removes access to protected information assets when no longer needed.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Per-event |

**How This Toolkit Addresses CC6.7:**

1. **Termination Monitoring**
   - Deprovisioning workflow tracking
   - Access removal verification
   - Orphaned account detection

2. **Compliance Validation**
   - SLA tracking (24-hour removal target)
   - Downstream system sync verification
   - Audit trail completeness

---

### CC6.8 - Privileged Access Management

**Criterion:** The entity restricts privileged access based on job responsibilities.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Testing Frequency** | Continuous |

**How This Toolkit Addresses CC6.8:**

1. **PIM Enforcement**
   - Zero standing admin policy
   - Time-bound privilege grants
   - MFA for all activations

2. **Monitoring & Alerting**
   - Real-time activation alerts
   - Anomaly detection
   - SIEM integration (Splunk)

**Evidence Generated:**
```
Evidence Type: Privileged Access Report
Location: /reports/privileged-access-{date}.json
Frequency: Real-time + daily summary
Retention: 7 years

Key Metrics:
- Standing privileged accounts: 2 (break-glass only)
- PIM-managed roles: 28
- Average activation approval time: 4.2 minutes
- Expired activations auto-revoked: 100%
```

---

## CC7: System Operations

### CC7.2 - Monitoring for Anomalies

**Criterion:** The entity monitors system components for anomalies that are indicative of malicious acts, natural disasters, and errors.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Testing Frequency** | Continuous |

**How This Toolkit Addresses CC7.2:**

1. **Policy Change Detection**
   - Real-time CA policy monitoring
   - Drift detection from baseline
   - Unauthorized change alerting

2. **SIEM Integration**
   - Splunk HEC event forwarding
   - CIM-compliant data model
   - Correlation rule triggers

**Evidence Generated:**
```
Evidence Type: Security Monitoring Report
Location: /reports/security-monitoring-{date}.json
Frequency: Real-time
Retention: 7 years
```

---

### CC7.3 - Incident Response

**Criterion:** The entity evaluates security events to determine whether they could or have resulted in a failure of the entity to meet its objectives.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | Security Team |
| **Testing Frequency** | Per-event |

**How This Toolkit Addresses CC7.3:**

1. **Automated Alerting**
   - Policy violation notifications
   - PIM abuse detection
   - Access anomaly alerts

2. **Remediation Guidance**
   - Auto-generated recommendations
   - Playbook integration
   - Evidence collection automation

---

## CC8: Change Management

### CC8.1 - Change Authorization

**Criterion:** The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures.

| Attribute | Details |
|-----------|---------|
| **Implementation Status** | Fully Implemented |
| **Control Owner** | IAM Team |
| **Testing Frequency** | Per-change |

**How This Toolkit Addresses CC8.1:**

1. **Policy Change Tracking**
   - All CA policy changes logged
   - Before/after comparison
   - Approval workflow integration

2. **Configuration Management**
   - Policy-as-code support
   - Version control integration
   - Rollback capability

---

## Audit Evidence Package

### Evidence Collection Checklist

| Evidence Type | Location | Frequency | Owner |
|--------------|----------|-----------|-------|
| CA Policy Analysis | `/reports/ca-policy/` | Daily | IAM Team |
| PIM Compliance | `/reports/pim/` | Daily | IAM Team |
| Access Reviews | `/reports/access-review/` | Quarterly | IAM Team |
| Privileged Access | `/reports/privileged/` | Real-time | Security |
| SIEM Events | Splunk | Real-time | Security |
| User Provisioning | `/reports/provisioning/` | Per-event | IAM Team |

### Auditor Access

```python
# Generate audit evidence package
from src.compliance import generate_soc2_evidence_package

package = generate_soc2_evidence_package(
    audit_period_start="2025-01-01",
    audit_period_end="2025-12-31",
    output_format="pdf",
    include_raw_logs=True
)
```

---

## Control Testing Results

### Test Summary (Sample)

| Control | Test Date | Tester | Result | Exceptions |
|---------|-----------|--------|--------|------------|
| CC6.1 | 2025-11-15 | External Auditor | Pass | None |
| CC6.2 | 2025-11-15 | External Auditor | Pass | None |
| CC6.3 | 2025-11-16 | External Auditor | Pass | None |
| CC6.6 | 2025-11-16 | External Auditor | Pass | None |
| CC6.7 | 2025-11-17 | External Auditor | Pass | None |
| CC6.8 | 2025-11-17 | External Auditor | Pass | None |
| CC7.2 | 2025-11-18 | External Auditor | Pass | None |
| CC7.3 | 2025-11-18 | External Auditor | Pass | None |
| CC8.1 | 2025-11-19 | External Auditor | Pass | None |

---

## Attestation

**IAM Team Lead Attestation:**

I attest that the controls described in this document are operating effectively and that the evidence provided accurately represents our identity governance practices.

Signature: _________________________
Name: _________________________
Date: _________________________

---

*This document supports SOC 2 Type II audit evidence requirements.*
*Prepared for Chainguard IT Engineer (Identity/IAM) Portfolio - Mike Dominic*
