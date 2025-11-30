# Entra ID Governance Concepts

This document explains the key identity governance concepts implemented in this toolkit.

## Table of Contents

1. [Conditional Access](#conditional-access)
2. [Privileged Identity Management (PIM)](#privileged-identity-management-pim)
3. [Access Reviews](#access-reviews)
4. [Entitlement Management](#entitlement-management)
5. [Identity Governance](#identity-governance)

---

## Conditional Access

### What is Conditional Access?

Conditional Access is Microsoft's Zero Trust policy engine. It evaluates signals (user, location, device, risk) and makes real-time access decisions to enforce security controls.

### Key Components

**Conditions (IF):**
- **Users/Groups** - Who is trying to access?
- **Cloud Apps** - What are they trying to access?
- **Locations** - Where are they accessing from?
- **Device State** - Is the device compliant/managed?
- **Client Apps** - Which protocol/app are they using?
- **Sign-in Risk** - Is the sign-in risky?

**Controls (THEN):**
- **Grant** - Block, require MFA, require compliant device, etc.
- **Session** - Sign-in frequency, app-enforced restrictions

### Common Policies

1. **Require MFA for all users**
   ```
   IF: All users accessing all cloud apps
   THEN: Grant access with MFA
   ```

2. **Block legacy authentication**
   ```
   IF: All users using legacy auth protocols
   THEN: Block access
   ```

3. **Require compliant devices**
   ```
   IF: All users accessing corporate apps
   THEN: Grant access with compliant device
   ```

### Policy States

- **Enabled** - Actively enforcing
- **Disabled** - Not enforcing
- **Report-only** - Logging but not enforcing (testing mode)

### Best Practices

- Start with report-only mode
- Exclude break-glass accounts
- Test before enabling
- Use named locations
- Block legacy authentication
- Require MFA for all users

---

## Privileged Identity Management (PIM)

### What is PIM?

PIM provides just-in-time (JIT) privileged access to Azure AD roles and Azure resources. Instead of permanent admin rights, users activate roles when needed for a limited time.

### Core Concepts

**Eligible vs Active:**
- **Eligible** - User can activate the role (requires PIM)
- **Active** - User currently has the role (standing access)

**Just-in-Time Access:**
Users request role activation → Approval (optional) → Time-limited access (e.g., 8 hours)

**Zero Standing Privilege:**
No permanent admin rights. All privileged access is temporary and audited.

### Critical Roles (Should Always Use PIM)

- Global Administrator
- Privileged Role Administrator
- Security Administrator
- User Administrator
- Exchange Administrator
- SharePoint Administrator
- Application Administrator
- Cloud Application Administrator

### PIM Activation Flow

```
1. User identifies need for privileged access
2. User requests role activation in PIM
3. Provides justification and ticket number
4. [Optional] Approval by role owner
5. Role activated for specified duration (1-8 hours)
6. User performs admin tasks
7. Role automatically deactivates after duration
8. All actions are audited
```

### PIM Settings

**Activation:**
- Maximum duration (1-24 hours)
- Require justification
- Require ticket number
- Require approval
- Require MFA on activation

**Assignment:**
- Maximum eligible duration
- Require justification for assignment
- Approval for assignment

**Notification:**
- Email on activation
- Email on assignment
- Alert on suspicious activation

### Standing Access Violations

**What is it?**
When a critical role has permanent (active) assignment instead of eligible (PIM) assignment.

**Why is it bad?**
- Violates least privilege principle
- Increases attack surface
- No audit trail of when admin rights were used
- Violates many compliance frameworks

**How this toolkit detects it:**
Checks if critical roles have active assignments with no end date or end date > 1 year in the future.

---

## Access Reviews

### What are Access Reviews?

Periodic certification of user access to ensure users only have access they still need.

### Review Types

**Group Membership Reviews:**
- Review who has access to sensitive groups
- Common for admin groups, data access groups

**Application Access Reviews:**
- Review who can access specific applications
- Common for privileged applications

**Azure AD Role Reviews:**
- Review who has administrative roles
- Critical for security and compliance

**Guest User Reviews:**
- Review external user access
- Ensure external users still need access

### Review Configuration

**Reviewers:**
- **Manager** - User's direct manager
- **Group owners** - Owners of the group
- **Selected reviewers** - Specific people
- **Self-review** - Users review themselves

**Settings:**
- **Recurrence** - One-time, weekly, monthly, quarterly, annually
- **Duration** - How long reviewers have to complete (e.g., 14 days)
- **Auto-apply** - Automatically remove access if denied
- **Default decision** - If reviewer doesn't respond (approve/deny/recommendation)
- **Justification required** - Require explanation for decisions

### Review Process

```
1. Access review is created/started
2. Reviewers receive email notification
3. Reviewers make decisions:
   - Approve (continue access)
   - Deny (remove access)
   - Don't know (neutral)
4. Review completes after duration
5. Decisions are applied (if auto-apply enabled)
6. Results are logged for audit
```

### Best Practices

- Review critical groups quarterly
- Require justification for all approvals
- Enable auto-apply to enforce decisions
- Send reminders to reviewers
- Review the reviewers - ensure appropriate people
- Track completion rates

---

## Entitlement Management

### What is Entitlement Management?

Self-service access request workflow system. Users request access packages instead of asking IT.

### Key Components

**Access Package:**
Bundle of resources (groups, apps, SharePoint sites) users can request

**Catalog:**
Container for access packages and resources

**Policy:**
Rules for who can request, approval requirements, access duration

### Example

**Access Package:** "Marketing Campaign Tools"
- Resources: Marketing SharePoint site, Adobe Creative Cloud, Marketing email group
- Policy: Any marketing employee can request, manager approval required, 90-day access

### Benefits

- Self-service reduces IT burden
- Consistent access processes
- Automated provisioning/deprovisioning
- Audit trail of all access requests
- Time-limited access by default

---

## Identity Governance

### The Big Picture

Identity Governance is about managing the identity lifecycle and access lifecycle:

**Identity Lifecycle:**
1. Hire (provision accounts)
2. Change (update access as role changes)
3. Leave (deprovision accounts)

**Access Lifecycle:**
1. Request (how users get access)
2. Approve (who authorizes access)
3. Review (periodic certification)
4. Revoke (remove when no longer needed)

### Zero Trust Principles

1. **Verify explicitly** - Always authenticate and authorize
2. **Least privilege** - Limit access to minimum needed
3. **Assume breach** - Minimize blast radius

### How This Toolkit Helps

**Conditional Access:**
- Implements "verify explicitly"
- Enforces device compliance, MFA, location controls

**PIM:**
- Implements "least privilege"
- Eliminates standing admin access
- Time-limited privileged access

**Access Reviews:**
- Ensures access remains appropriate
- Regular certification of permissions
- Removes unnecessary access

**Compliance Reporting:**
- Proves governance controls are working
- Identifies gaps and violations
- Provides evidence for auditors

---

## Compliance Frameworks

This toolkit helps meet requirements for:

**SOC 2:**
- CC6.1 - Logical access controls
- CC6.2 - Prior to granting access
- CC6.3 - Removes access when no longer needed

**ISO 27001:**
- A.9.2.1 - User registration and deregistration
- A.9.2.2 - User access provisioning
- A.9.2.5 - Review of user access rights
- A.9.2.6 - Removal of access rights

**NIST 800-53:**
- AC-2 - Account Management
- AC-6 - Least Privilege
- AC-6(2) - Privileged Access for Non-organizational Users

**PCI DSS:**
- 7.1 - Limit access to system components
- 7.2 - Establish an access control system
- 8.1.4 - Remove/disable inactive accounts

---

## Glossary

**Break Glass Account** - Emergency admin account excluded from CA policies

**Eligible Assignment** - PIM role that can be activated

**Grant Controls** - CA policy controls that grant access (MFA, compliant device)

**Just-in-Time (JIT)** - Temporary access granted when needed

**Named Location** - IP ranges defined in CA for location-based policies

**Privileged Access** - Administrative/high-permission access

**Report-Only Mode** - CA policy logs but doesn't enforce

**Session Controls** - CA policy controls during active session

**Standing Access** - Permanent role assignment (anti-pattern for admins)

**Zero Standing Privilege (ZSP)** - No permanent admin rights, all via PIM

---

## Further Reading

- [Microsoft Entra ID Documentation](https://learn.microsoft.com/en-us/azure/active-directory/)
- [Conditional Access Documentation](https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/)
- [PIM Documentation](https://learn.microsoft.com/en-us/azure/active-directory/privileged-identity-management/)
- [Zero Trust Architecture](https://www.microsoft.com/en-us/security/business/zero-trust)
