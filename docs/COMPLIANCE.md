# Compliance Mapping - Entra ID Governance Toolkit

## Executive Summary

Entra ID Governance Toolkit is a comprehensive Microsoft Entra ID (formerly Azure AD) identity governance automation platform for policy analysis, Privileged Identity Management (PIM), and access reviews. This document maps the platform's capabilities to major compliance frameworks including NIST 800-53, SOC 2, ISO 27001, and CIS Controls.

**Overall Compliance Posture:**
- **NIST 800-53**: 44 controls mapped across AC, AU, IA, IR, RA families
- **SOC 2 Type II**: Strong alignment with CC6, CC7, CC8 criteria
- **ISO 27001:2022**: Coverage for A.5, A.8, A.9, A.12 controls
- **CIS Controls v8**: Implementation of Controls 5, 6, 8, 14, 16

## NIST 800-53 Control Mapping

### AC (Access Control) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| AC-2 | Account Management | Fully Implemented | Conditional Access policy analysis; Standing admin access detection; PIM compliance scoring | None |
| AC-2(4) | Automated Audit Actions | Fully Implemented | Automated policy violation detection; Microsoft Graph API integration for continuous monitoring | None |
| AC-2(7) | Role-Based Schemes | Fully Implemented | PIM role assignment analysis; Azure AD role governance | None |
| AC-2(11) | Usage Conditions | Fully Implemented | Conditional Access policy enforcement monitoring; Terms of use compliance | None |
| AC-2(12) | Account Monitoring | Fully Implemented | Continuous CA policy monitoring; PIM activation tracking | None |
| AC-3 | Access Enforcement | Fully Implemented | Conditional Access policy coverage analysis; Security posture scoring (0-100) | None |
| AC-5 | Separation of Duties | Fully Implemented | PIM detects excessive role assignments; Conflicting permission identification | None |
| AC-6 | Least Privilege | Fully Implemented | PIM just-in-time (JIT) role activation; Standing privilege violation detection | None |
| AC-6(2) | Non-Privileged Access | Fully Implemented | Separation of privileged and standard user access; Break glass account exclusion | None |
| AC-6(5) | Privileged Accounts | Fully Implemented | PIM enforces time-bound privileged access; Activation history tracking | None |
| AC-6(9) | Log Use of Privileged Functions | Fully Implemented | PIM activation logging; Admin action audit trails | None |
| AC-17 | Remote Access | Fully Implemented | CA policies for remote access scenarios; Location-based access controls | None |

### AU (Audit and Accountability) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| AU-2 | Audit Events | Fully Implemented | Microsoft Graph API audit log collection; CA policy change tracking | None |
| AU-3 | Content of Audit Records | Fully Implemented | Logs include user, policy, action, timestamp, result, device, location | None |
| AU-6 | Audit Review, Analysis, and Reporting | Fully Implemented | Automated policy analysis; Coverage gap detection; Compliance reporting | None |
| AU-6(1) | Process Integration | Fully Implemented | FastAPI REST endpoints for SIEM integration; Webhook support | None |
| AU-6(3) | Correlate Audit Repositories | Fully Implemented | Cross-policy correlation; Conflict identification | None |
| AU-7 | Audit Reduction and Report Generation | Fully Implemented | Dashboard filtering by severity; CSV/JSON export capabilities | None |
| AU-9 | Protection of Audit Information | Fully Implemented | Immutable Microsoft Graph audit logs; RBAC for log access | None |
| AU-12 | Audit Generation | Fully Implemented | Comprehensive event logging via Microsoft Graph | None |

### IA (Identification and Authentication) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| IA-2 | Identification and Authentication | Fully Implemented | CA policy enforcement for authentication; MFA requirement analysis | None |
| IA-2(1) | Network Access to Privileged Accounts | Fully Implemented | PIM MFA enforcement for admin roles; CA policies for privileged access | None |
| IA-2(2) | Network Access to Non-Privileged Accounts | Fully Implemented | CA policy coverage for all users; MFA gap detection | None |
| IA-2(5) | Group Authentication | Fully Implemented | Group-based CA policies; Access review by group membership | None |
| IA-2(8) | Replay-Resistant Authentication | Fully Implemented | Token-based authentication monitoring; Session management policies | None |
| IA-4 | Identifier Management | Fully Implemented | User identity tracking; Account lifecycle governance | None |
| IA-5 | Authenticator Management | Fully Implemented | MFA method enforcement analysis; Passwordless authentication support | None |

### IR (Incident Response) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| IR-4 | Incident Handling | Fully Implemented | Automated remediation recommendations; Policy violation alerting | None |
| IR-5 | Incident Monitoring | Fully Implemented | Real-time policy change detection; Access review monitoring | None |
| IR-6 | Incident Reporting | Fully Implemented | Compliance reports; Executive dashboards | None |

### RA (Risk Assessment) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| RA-3 | Risk Assessment | Fully Implemented | Security posture scoring; PIM compliance scoring; Risk assessment analysis | None |
| RA-5 | Vulnerability Scanning | Fully Implemented | CA policy coverage gaps; Misconfigurations identification; Standing admin detection | None |
| RA-5(3) | Breadth/Depth of Coverage | Fully Implemented | Comprehensive CA policy analysis; PIM entitlement governance | None |

### SC (System and Communications Protection) Family

| Control ID | Control Name | Implementation | Features | Gaps |
|------------|--------------|----------------|----------|------|
| SC-8 | Transmission Confidentiality | Fully Implemented | TLS for Microsoft Graph API; Secure token handling | None |
| SC-13 | Cryptographic Protection | Fully Implemented | MSAL token encryption; Secure credential storage | None |

## SOC 2 Type II Trust Services Criteria

### CC6: Logical and Physical Access Controls

| Criterion | Implementation | Evidence | Gaps |
|-----------|----------------|----------|------|
| CC6.1 - Access restricted to authorized users | Fully Implemented | CA policy analysis ensures access restrictions; PIM prevents standing admin access | None |
| CC6.2 - Authentication mechanisms | Fully Implemented | CA policy enforcement validation; MFA requirement monitoring | None |
| CC6.3 - Authorization mechanisms | Fully Implemented | PIM role assignment governance; Just-in-time access enforcement | None |
| CC6.6 - Access monitoring | Fully Implemented | Continuous policy monitoring; Access review completion tracking | None |
| CC6.7 - Access removal | Fully Implemented | Access review automation; Overdue review detection | None |
| CC6.8 - Privileged access | Fully Implemented | PIM standing admin detection; JIT privilege enforcement | None |

### CC7: System Operations

| Criterion | Implementation | Evidence | Gaps |
|-----------|----------------|----------|------|
| CC7.2 - System monitoring | Fully Implemented | FastAPI health checks; Policy drift detection | None |
| CC7.3 - Incident response | Fully Implemented | Automated violation alerting; Remediation recommendations | None |

### CC8: Change Management

| Criterion | Implementation | Evidence | Gaps |
|-----------|----------------|----------|------|
| CC8.1 - Change authorization | Fully Implemented | CA policy change tracking; Unauthorized modification detection | None |

## ISO 27001:2022 Annex A Controls

### A.5 Information Security Policies

| Control | Name | Implementation | Features | Gaps |
|---------|------|----------------|----------|------|
| A.5.1 | Policies for information security | Fully Implemented | CA policy framework analysis; Policy enforcement monitoring | None |
| A.5.3 | Segregation of duties | Fully Implemented | PIM role conflict detection; Excessive privilege identification | None |

### A.8 Asset Management

| Control | Name | Implementation | Features | Gaps |
|---------|------|----------------|----------|------|
| A.8.1 | Responsibility for assets | Fully Implemented | Identity asset inventory; Access review ownership tracking | None |
| A.8.2 | Information classification | Fully Implemented | Sensitive role identification; High-risk access monitoring | None |

### A.9 Access Control

| Control | Name | Implementation | Features | Gaps |
|---------|------|----------------|----------|------|
| A.9.1 | Business requirements for access control | Fully Implemented | CA policy requirement validation; Compliance gap identification | None |
| A.9.2 | User access management | Fully Implemented | Access review automation; User lifecycle governance | None |
| A.9.3 | User responsibilities | Fully Implemented | Individual access accountability; Audit trail per user | None |
| A.9.4 | System and application access control | Fully Implemented | Application-specific CA policies; Scope-based authorization | None |

### A.12 Operations Security

| Control | Name | Implementation | Features | Gaps |
|---------|------|----------------|----------|------|
| A.12.1 | Operational procedures | Fully Implemented | Documented governance workflows; Runbook automation | None |
| A.12.4 | Logging and monitoring | Fully Implemented | Microsoft Graph audit logging; Real-time event monitoring | None |

## CIS Controls v8

| Control | Name | Implementation | Features | Gaps |
|---------|------|----------------|----------|------|
| 5.1 | Establish and Maintain an Inventory of Accounts | Fully Implemented | Entra ID user inventory; PIM role assignment tracking | None |
| 5.3 | Disable Dormant Accounts | Fully Implemented | Inactive user detection; Lifecycle policy enforcement | None |
| 5.4 | Restrict Administrator Privileges | Fully Implemented | PIM JIT admin access; Standing privilege detection and remediation | None |
| 5.5 | Establish and Maintain MFA | Fully Implemented | CA policy MFA enforcement; Coverage gap analysis | None |
| 6.1 | Establish Access Control Mechanisms | Fully Implemented | CA policy framework; Centralized access governance | None |
| 6.2 | Establish Least Privilege | Fully Implemented | PIM enforces least privilege; Excessive role assignment detection | None |
| 6.8 | Define and Maintain RBAC | Fully Implemented | Azure AD role-based access; Group-based policy enforcement | None |
| 8.2 | Collect Audit Logs | Fully Implemented | Microsoft Graph audit log collection; Comprehensive event tracking | None |
| 8.5 | Collect Detailed Audit Logs | Fully Implemented | Detailed CA policy logs; PIM activation history | None |
| 8.11 | Conduct Audit Log Reviews | Fully Implemented | Automated log analysis; Policy violation detection | None |
| 14.3 | Controlled Access to Security Infrastructure | Fully Implemented | Break glass account monitoring; Emergency access governance | None |
| 16.1 | Establish Account Audit Process | Fully Implemented | Access review automation; Completion rate tracking | None |
| 16.6 | Maintain Inventory of Accounts | Fully Implemented | Real-time identity inventory via Microsoft Graph | None |

## Conditional Access Policy Compliance

### NIST 800-53 CA Policy Mapping

| Control ID | CA Policy Feature | Implementation |
|------------|------------------|----------------|
| AC-2(11) | Usage Conditions | Terms of use enforcement; Conditional access based on compliance state |
| AC-3 | Access Enforcement | Grant/block controls; Session controls; Application enforcement |
| AC-17 | Remote Access | Location-based policies; Trusted network requirements |
| IA-2(1) | MFA - Privileged | MFA enforcement for admin roles; Risk-based step-up authentication |
| IA-2(8) | Replay Resistance | Token binding; Session lifetime controls |
| SC-7 | Boundary Protection | Network location conditions; Trusted IP ranges |

### SOC 2 CA Policy Controls

| Criterion | CA Policy Feature | Compliance Value |
|-----------|------------------|-----------------|
| CC6.1 | User/group targeting | Ensures only authorized users access resources |
| CC6.2 | Authentication strength | MFA enforcement; Passwordless authentication |
| CC6.3 | Grant controls | Granular access decisions; Conditional approval |
| CC6.6 | Sign-in monitoring | Real-time authentication monitoring; Risk detection |

## Privileged Identity Management (PIM) Compliance

### NIST 800-53 PIM Mapping

| Control ID | PIM Feature | Implementation |
|------------|-------------|----------------|
| AC-2(7) | Role-Based Access | Azure AD role assignments; PIM eligibility tracking |
| AC-6 | Least Privilege | Time-bound role activation; JIT access enforcement |
| AC-6(5) | Privileged Accounts | Eligible vs. active assignments; Activation justification |
| AC-6(9) | Privileged Function Logging | PIM activation history; Audit trail for all role changes |
| AU-6 | Audit Analysis | PIM compliance scoring; Standing admin violation reports |

### SOC 2 PIM Controls

| Criterion | PIM Feature | Compliance Value |
|-----------|-------------|-----------------|
| CC6.8 | JIT privileged access | Eliminates standing admin privileges |
| CC6.1 | Approval workflows | Multi-approver requirement for sensitive roles |
| CC6.6 | Activation monitoring | Real-time tracking of privilege escalation |
| CC7.2 | Compliance reporting | PIM violation detection and remediation tracking |

## Access Review Compliance

### NIST 800-53 Access Review Mapping

| Control ID | Access Review Feature | Implementation |
|------------|---------------------|----------------|
| AC-2(4) | Automated Audits | Scheduled access reviews; Automated recertification |
| AC-2(7) | Role-Based Reviews | Group membership reviews; Role assignment validation |
| AU-6 | Review Analysis | Completion rate tracking; Overdue review detection |

### SOC 2 Access Review Controls

| Criterion | Access Review Feature | Compliance Value |
|-----------|---------------------|-----------------|
| CC6.7 | Periodic reviews | Ensures timely access removal for terminated/transferred users |
| CC6.1 | Access validation | Confirms access remains appropriate for job function |
| CC7.2 | Review monitoring | Tracks reviewer performance and compliance |

## Compliance Gaps and Roadmap

### Current Gaps

1. **Multi-Tenant Support** - Single tenant currently; MSP support in roadmap
2. **Real-Time Alerting** - Dashboard-based; Teams/email alerts planned
3. **Historical Trend Analysis** - Point-in-time analysis; database storage planned

### Roadmap for Full Compliance

**Phase 2 (Next 6 months):**
- Multi-tenant governance support
- Real-time Microsoft Teams alerting
- ServiceNow webhook integration
- Advanced threat detection via Microsoft Defender

**Phase 3 (12 months):**
- Historical trend database (PostgreSQL)
- React dashboard frontend
- Azure DevOps integration
- Terraform/Bicep deployment templates
- Compliance report scheduling and automation

## Evidence Collection for Audits

### Automated Evidence Generation

The platform provides audit-ready evidence through:

1. **FastAPI Endpoints:**
   ```bash
   # Conditional Access policy analysis
   curl http://localhost:8000/api/v1/policies/analysis/coverage

   # PIM violation detection
   curl http://localhost:8000/api/v1/pim/analysis/violations

   # Access review completion
   curl http://localhost:8000/api/v1/reviews/completion

   # Full compliance report
   curl http://localhost:8000/api/v1/reports/compliance
   ```

2. **PowerShell Reports:**
   ```powershell
   .\powershell\Get-ConditionalAccessPolicies.ps1 -ExportPath "ca_policies.json"
   .\powershell\Export-PIMAssignments.ps1 -ExportPath "pim_assignments.csv"
   ```

3. **Compliance Reports:**
   - Security posture scoring (0-100)
   - Policy coverage gap analysis
   - PIM compliance metrics
   - Access review completion rates

### Audit Preparation Checklist

- [ ] Export CA policy configurations (last 90 days of changes)
- [ ] Generate PIM violation reports
- [ ] Collect access review completion evidence
- [ ] Document security posture trends
- [ ] Review and document remediation actions
- [ ] Prepare Microsoft Graph API integration evidence

## Microsoft Graph API Compliance

### API Permissions and Least Privilege

| Permission | Scope | Justification | Compliance Control |
|------------|-------|---------------|-------------------|
| Policy.Read.All | Application | Read CA policies | AC-3, RA-5 |
| RoleManagement.Read.All | Application | Read PIM assignments | AC-6, CC6.8 |
| AccessReview.Read.All | Application | Monitor access reviews | AC-2(4), CC6.7 |
| Directory.Read.All | Application | User/group inventory | CIS 5.1, A.9.2 |

All permissions follow least-privilege principle (read-only where possible).

### API Security Controls

| Control | Implementation | Compliance Benefit |
|---------|----------------|-------------------|
| Client credential flow | App registration with secret | NIST IA-2, SC-8 |
| Token caching | MSAL token management | SC-13, CC6.2 |
| Retry with backoff | Exponential backoff on 429/503 | CC7.4 |
| Error handling | Graceful degradation on API failures | CC7.2 |

## Cost Analysis for Compliance Budget

**Monthly Operational Cost: Variable (Entra ID License-Dependent)**

| Component | Cost | Compliance Value |
|-----------|------|-----------------|
| Entra ID Free | $0 | Basic CA policies, limited PIM |
| Entra ID P1 | $6/user/month | Full CA policies, conditional access |
| Entra ID P2 | $9/user/month | PIM, access reviews, identity protection |
| Microsoft Graph API | Free | Unlimited API calls for compliance automation |
| FastAPI Server | $0 (self-hosted) | REST interface for SIEM integration |

**Recommendation**: Entra ID P2 required for full compliance features (PIM, access reviews).

## Conclusion

Entra ID Governance Toolkit provides comprehensive compliance coverage for Microsoft identity governance and administration. The platform's automated policy analysis, PIM enforcement, and access review capabilities align with 44+ NIST controls, SOC 2 criteria, ISO 27001 requirements, and CIS Controls.

Key compliance strengths:
- **Conditional Access governance** (NIST AC-3, SOC 2 CC6.1)
- **Privileged Identity Management** (NIST AC-6(5), ISO A.9.2)
- **Access review automation** (NIST AC-2(4), CIS 16.1)
- **Security posture scoring** (NIST RA-3, SOC 2 CC7.2)
- **Comprehensive audit trails** (NIST AU-2, AU-12)
- **Just-in-time privileged access** (NIST AC-6, CC6.8)

The combination of automated analysis, policy enforcement monitoring, and compliance reporting makes this toolkit suitable for enterprise Entra ID governance and regulatory compliance.

For questions regarding specific compliance requirements or audit preparation, refer to the evidence collection section or review the deployment evidence documentation.
