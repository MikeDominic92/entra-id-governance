# Audit Evidence Generator

> **Chainguard Relevance:** This document demonstrates expertise in "preparing evidence for SOC 2, ISO27001, and other regulatory audits" - a key requirement for IT Engineer (Identity/IAM) roles.

## Overview

The Audit Evidence Generator automates the collection, formatting, and packaging of compliance evidence for external auditors. It supports SOC 2, ISO 27001, NIST, and other regulatory frameworks.

## Quick Start

### Generate Evidence Package

```python
from src.compliance.evidence_generator import AuditEvidenceGenerator

# Initialize generator
generator = AuditEvidenceGenerator(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

# Generate SOC 2 evidence package
soc2_package = generator.generate_soc2_package(
    audit_period_start="2025-01-01",
    audit_period_end="2025-12-31",
    output_path="./audit-evidence/soc2-2025/"
)

# Generate ISO 27001 evidence package
iso_package = generator.generate_iso27001_package(
    audit_year=2025,
    controls=["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.2"],
    output_path="./audit-evidence/iso27001-2025/"
)
```

## Evidence Types

### 1. Conditional Access Policy Evidence

```python
# Generate CA policy evidence
ca_evidence = generator.generate_ca_policy_evidence(
    include_screenshots=True,
    include_raw_json=True
)
```

**Output Contents:**
```
ca-policy-evidence/
├── summary-report.pdf           # Executive summary
├── policy-inventory.json        # All policies with details
├── coverage-analysis.json       # Gap analysis
├── mfa-enforcement-report.json  # MFA coverage
├── legacy-auth-report.json      # Legacy auth status
└── screenshots/                 # Portal screenshots
    ├── policy-list.png
    ├── mfa-policy-config.png
    └── block-legacy-auth.png
```

### 2. PIM Compliance Evidence

```python
# Generate PIM evidence
pim_evidence = generator.generate_pim_evidence(
    include_activation_logs=True,
    days_back=365
)
```

**Output Contents:**
```
pim-evidence/
├── standing-admin-report.pdf    # Zero standing admin proof
├── role-inventory.json          # All PIM-managed roles
├── activation-history.json      # All activations
├── activation-summary.pdf       # Statistical summary
├── average-duration-report.json # Duration metrics
└── justification-samples.json   # Sample justifications
```

### 3. Access Review Evidence

```python
# Generate access review evidence
review_evidence = generator.generate_access_review_evidence(
    campaigns=["Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"],
    include_individual_decisions=True
)
```

**Output Contents:**
```
access-review-evidence/
├── campaign-summary.pdf         # All campaigns summary
├── Q1-2025/
│   ├── campaign-details.json
│   ├── reviewer-list.json
│   ├── decisions.json
│   └── completion-report.pdf
├── Q2-2025/
│   └── ...
├── Q3-2025/
│   └── ...
└── Q4-2025/
    └── ...
```

### 4. User Lifecycle Evidence

```python
# Generate lifecycle evidence
lifecycle_evidence = generator.generate_lifecycle_evidence(
    include_provisioning=True,
    include_deprovisioning=True,
    sample_size=50
)
```

**Output Contents:**
```
lifecycle-evidence/
├── provisioning-summary.pdf     # Onboarding metrics
├── deprovisioning-summary.pdf   # Offboarding metrics
├── sla-compliance.json          # SLA adherence
├── sample-provisions.json       # Sample records
└── sample-deprovisions.json     # Sample records
```

### 5. SIEM Integration Evidence

```python
# Generate SIEM evidence
siem_evidence = generator.generate_siem_evidence(
    siem_type="splunk",
    sample_events=100
)
```

**Output Contents:**
```
siem-evidence/
├── integration-config.json      # HEC configuration
├── event-flow-diagram.png       # Architecture
├── sample-events.json           # Event samples
├── alert-rules.json             # Correlation rules
└── dashboard-screenshots/       # Splunk dashboards
    ├── identity-overview.png
    └── privileged-access.png
```

## Complete Audit Package

### SOC 2 Type II Package

```python
package = generator.generate_complete_soc2_package(
    audit_period_start="2025-01-01",
    audit_period_end="2025-12-31",
    output_path="./soc2-audit-2025/"
)
```

**Package Contents:**
```
soc2-audit-2025/
├── README.md                    # Package guide
├── executive-summary.pdf        # Management summary
├── control-matrix.xlsx          # Control mapping
│
├── CC6-logical-access/
│   ├── CC6.1-access-security/
│   ├── CC6.2-authentication/
│   ├── CC6.3-authorization/
│   ├── CC6.6-access-monitoring/
│   ├── CC6.7-access-removal/
│   └── CC6.8-privileged-access/
│
├── CC7-system-operations/
│   ├── CC7.2-monitoring/
│   └── CC7.3-incident-response/
│
├── CC8-change-management/
│   └── CC8.1-change-authorization/
│
├── supporting-evidence/
│   ├── policies/
│   ├── procedures/
│   └── screenshots/
│
└── attestations/
    ├── iam-team-attestation.pdf
    └── management-attestation.pdf
```

### ISO 27001 Package

```python
package = generator.generate_complete_iso27001_package(
    audit_year=2025,
    output_path="./iso27001-audit-2025/"
)
```

**Package Contents:**
```
iso27001-audit-2025/
├── README.md
├── statement-of-applicability.xlsx
├── executive-summary.pdf
│
├── A.5-organizational/
│   ├── A.5.15-access-control/
│   ├── A.5.16-identity-management/
│   ├── A.5.17-authentication/
│   └── A.5.18-access-rights/
│
├── A.6-people/
│   ├── A.6.1-screening/
│   └── A.6.5-termination/
│
├── A.8-technological/
│   ├── A.8.2-privileged-access/
│   ├── A.8.3-access-restriction/
│   ├── A.8.5-authentication/
│   ├── A.8.15-logging/
│   └── A.8.16-monitoring/
│
└── internal-audit-reports/
    ├── 2025-Q2-internal-audit.pdf
    └── 2025-Q3-internal-audit.pdf
```

## Automated Evidence Collection

### Schedule Regular Collection

```python
from src.compliance.scheduler import EvidenceScheduler

scheduler = EvidenceScheduler(generator)

# Daily evidence collection
scheduler.schedule_daily(
    evidence_types=["ca_policies", "pim_activations"],
    time="02:00"  # 2 AM
)

# Weekly evidence collection
scheduler.schedule_weekly(
    evidence_types=["access_reviews", "lifecycle"],
    day="sunday",
    time="03:00"
)

# Monthly evidence package
scheduler.schedule_monthly(
    package_type="compliance_summary",
    day=1,
    time="04:00"
)
```

### Evidence Retention

```python
# Configure retention policy
generator.configure_retention(
    retention_years=7,
    archive_location="azure-blob://audit-evidence-archive",
    encryption_enabled=True
)
```

## Evidence Validation

### Pre-Audit Validation

```python
# Validate evidence completeness
validation = generator.validate_evidence_package(
    package_path="./soc2-audit-2025/",
    framework="SOC2"
)

print(validation)
# {
#   "status": "complete",
#   "controls_covered": 15,
#   "controls_required": 15,
#   "missing_evidence": [],
#   "warnings": ["Screenshot quality low for CC6.2"],
#   "recommendations": ["Add user interview documentation"]
# }
```

### Evidence Chain of Custody

```python
# Generate chain of custody log
custody_log = generator.generate_custody_log(
    package_id="SOC2-2025-001",
    include_hashes=True
)

print(custody_log)
# {
#   "package_id": "SOC2-2025-001",
#   "created_at": "2025-12-01T10:00:00Z",
#   "created_by": "iam-team@example.com",
#   "file_count": 247,
#   "total_size_mb": 156.3,
#   "sha256_manifest": "abc123...",
#   "access_log": [
#     {"timestamp": "2025-12-01T10:05:00Z", "user": "auditor@firm.com", "action": "download"}
#   ]
# }
```

## Integration with Audit Portals

### Upload to Auditor Portal

```python
# Upload evidence to common audit platforms
generator.upload_to_portal(
    portal="auditboard",  # or "workiva", "highbond"
    credentials={...},
    package_path="./soc2-audit-2025/"
)
```

## CLI Usage

```bash
# Generate SOC 2 evidence package
python -m src.compliance.cli generate-evidence \
  --framework soc2 \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --output ./audit-evidence/

# Validate evidence package
python -m src.compliance.cli validate \
  --package ./audit-evidence/soc2-2025/ \
  --framework soc2

# Generate executive summary
python -m src.compliance.cli summary \
  --package ./audit-evidence/soc2-2025/ \
  --format pdf
```

## Best Practices

### Evidence Quality

1. **Timestamp Everything** - All evidence must have clear timestamps
2. **Include Context** - Raw data plus explanatory summaries
3. **Use Screenshots Judiciously** - For UI-based controls
4. **Maintain Consistency** - Same format across audit periods
5. **Version Control** - Track changes to policies and procedures

### Auditor Expectations

1. **Organized Structure** - Clear folder hierarchy by control
2. **README Files** - Guide auditors through each section
3. **Cross-References** - Link related evidence across controls
4. **Completeness** - All population, not just samples
5. **Timeliness** - Evidence from within audit period

---

*This documentation supports compliance audit evidence preparation.*
*Prepared for Chainguard IT Engineer (Identity/IAM) Portfolio - Mike Dominic*
