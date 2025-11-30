# Cost Analysis

Understanding the costs associated with implementing Entra ID Governance features.

## Azure AD Licensing

### Required Licenses

**Azure AD Premium P2** (Required for full feature set)
- **Cost:** ~$9 USD per user/month
- **Includes:**
  - Conditional Access
  - Privileged Identity Management (PIM)
  - Access Reviews
  - Entitlement Management
  - Identity Protection
  - Identity Governance

**Alternative: Azure AD Premium P1**
- **Cost:** ~$6 USD per user/month
- **Includes:**
  - Conditional Access
  - NO PIM
  - NO Access Reviews
  - NO Entitlement Management

**Free Tier:**
- Basic Conditional Access (limited)
- No PIM, no Access Reviews
- **Not sufficient for this toolkit**

### Licensing Breakdown by Feature

| Feature | Free | P1 | P2 |
|---------|------|----|----|
| Conditional Access | Limited | ✓ | ✓ |
| PIM | ✗ | ✗ | ✓ |
| Access Reviews | ✗ | ✗ | ✓ |
| Entitlement Management | ✗ | ✗ | ✓ |
| Identity Protection | ✗ | ✗ | ✓ |

### Cost Calculation Example

**Organization:** 500 employees, 25 admins

**Option 1: P2 for Everyone**
- 500 users × $9/month = $4,500/month
- **Annual:** $54,000

**Option 2: P2 for Admins Only, P1 for Others**
- 25 admins × $9/month = $225/month
- 475 users × $6/month = $2,850/month
- **Total:** $3,075/month ($36,900/year)
- **Savings:** $17,100/year

**Recommendation:**
Assign P2 to:
- All administrators
- High-risk users (executives, HR, finance)
- Users requiring PIM
- Access review creators

Assign P1 to:
- General workforce
- Users only needing basic CA

## Infrastructure Costs

### This Toolkit

**Hosting Options:**

**Option 1: Run Locally**
- **Cost:** $0
- **Best for:** Testing, development, small-scale automation

**Option 2: Azure VM**
- **VM Size:** B2s (2 vCPU, 4 GB RAM)
- **Cost:** ~$30/month
- **Storage:** 64 GB SSD (~$2/month)
- **Total:** ~$32/month (~$384/year)

**Option 3: Azure App Service**
- **Tier:** Basic B1
- **Cost:** ~$55/month (~$660/year)
- **Includes:** Managed service, auto-scaling, deployment slots

**Option 4: Azure Container Instances**
- **Specs:** 1 vCPU, 1.5 GB memory
- **Cost:** ~$40/month (running 24/7)
- **Best for:** Containerized deployment

**Option 5: Azure Functions (Consumption Plan)**
- **Cost:** Pay-per-execution
- **First 1M executions free**
- **Typical:** $5-20/month
- **Best for:** Event-driven, scheduled tasks

### Additional Azure Services

**Azure Key Vault:**
- **Cost:** $0.03 per 10,000 operations
- **Typical usage:** <$5/month
- **Critical for:** Secret management

**Azure Log Analytics:**
- **Cost:** $2.76 per GB ingested (first 5 GB free)
- **Typical usage:** $10-30/month
- **Used for:** Centralized logging

**Azure Storage (for reports):**
- **Cost:** $0.018 per GB/month
- **Typical usage:** <$1/month

## API Costs

### Microsoft Graph API

**Pricing:** FREE
- No additional cost for Graph API calls
- Included with Azure AD licensing
- Rate limits apply (see below)

### Rate Limits

**Throttling Limits:**
- 2,000 requests/second per application
- 10,000 requests/10 minutes per user
- No charges for hitting limits (requests are just throttled)

**This toolkit includes:**
- Automatic retry with exponential backoff
- Batch request support
- Token caching

## Total Cost Examples

### Small Organization (100 users, 5 admins)

**Licensing:**
- 5 admins with P2: 5 × $9 = $45/month
- 95 users with P1: 95 × $6 = $570/month
- **Subtotal:** $615/month

**Infrastructure:**
- Azure Functions (scheduled): $10/month
- Azure Key Vault: $5/month
- **Subtotal:** $15/month

**Total:** $630/month ($7,560/year)

### Medium Organization (500 users, 25 admins)

**Licensing:**
- 25 admins with P2: 25 × $9 = $225/month
- 475 users with P1: 475 × $6 = $2,850/month
- **Subtotal:** $3,075/month

**Infrastructure:**
- Azure App Service B1: $55/month
- Azure Key Vault: $5/month
- Log Analytics: $20/month
- **Subtotal:** $80/month

**Total:** $3,155/month ($37,860/year)

### Large Organization (5,000 users, 100 admins)

**Licensing:**
- 100 admins with P2: 100 × $9 = $900/month
- 500 high-risk users with P2: 500 × $9 = $4,500/month
- 4,400 users with P1: 4,400 × $6 = $26,400/month
- **Subtotal:** $31,800/month

**Infrastructure:**
- Azure App Service P1V2: $146/month
- Azure Key Vault: $10/month
- Log Analytics: $100/month
- Storage: $5/month
- **Subtotal:** $261/month

**Total:** $32,061/month ($384,732/year)

## Cost Optimization Strategies

### 1. Targeted P2 Licensing

Only assign P2 to users who need:
- PIM (admins)
- Access Reviews (reviewers)
- Risk-based policies (executives, high-value targets)

**Savings:** 40-60% on licensing

### 2. Serverless Deployment

Use Azure Functions instead of always-on App Service:
- Only pay when code runs
- Great for scheduled reports
- Event-driven automation

**Savings:** $30-50/month on infrastructure

### 3. Efficient API Usage

- Implement caching (already included)
- Use batch requests
- Minimize unnecessary API calls

**Benefit:** Stay under rate limits, better performance

### 4. Right-Size Infrastructure

**For small deployments:**
- Run locally or on existing infrastructure
- Use serverless (Functions)

**For large deployments:**
- Use managed services (App Service)
- Implement auto-scaling
- Use reserved instances for predictable workloads

### 5. Trial Period

Microsoft offers:
- 30-day free trial of Azure AD Premium P2
- Test full feature set before committing
- Validate ROI before purchasing

## ROI Analysis

### Manual vs Automated Governance

**Without this toolkit:**
- Manual policy reviews: 8 hours/month @ $100/hr = $800/month
- PIM violations undetected: Security risk
- Access review reminders: 4 hours/month @ $75/hr = $300/month
- Compliance reporting: 16 hours/quarter @ $100/hr = $533/month
- **Total manual effort:** ~$1,633/month

**With this toolkit:**
- Infrastructure: $80/month
- Maintenance: 2 hours/month @ $100/hr = $200/month
- **Total automated cost:** $280/month

**Savings:** $1,353/month ($16,236/year)

### Security Benefits (Non-Monetary)

- Faster detection of standing admin access
- Consistent policy enforcement
- Reduced attack surface
- Better audit trail
- Improved compliance posture

### Avoided Costs

**Security Incident Prevention:**
- Average data breach cost: $4.45M (IBM 2023)
- Proper PIM reduces admin compromise risk by 80%
- Strong CA policies reduce phishing success by 99.9%

**Compliance Audit Savings:**
- Automated reporting saves 40-80 hours per audit
- Better evidence = faster audit completion
- Reduced audit findings = lower remediation costs

## Comparison with Alternatives

### Commercial IAM Tools

| Tool | Annual Cost (500 users) |
|------|------------------------|
| CyberArk Identity | $50,000 - $150,000 |
| Okta Identity Governance | $40,000 - $100,000 |
| SailPoint IdentityIQ | $75,000 - $200,000 |
| **Entra ID + This Toolkit** | **$37,860** |

**Advantage:** 60-80% cost savings using native Azure AD features

### Open Source Alternatives

| Tool | Licensing | Hosting | Maintenance |
|------|-----------|---------|-------------|
| Keycloak | Free | $500/year | 10 hrs/month |
| FreeIPA | Free | $500/year | 15 hrs/month |
| **This Toolkit** | **See above** | **$400/year** | **2 hrs/month** |

## Budget Recommendations

### Minimum Viable Setup

- Azure AD P2 for 10% of users (admins + high-risk): $450/month
- Azure AD P1 for 90% of users: $2,700/month
- Azure Functions deployment: $10/month
- **Total:** ~$3,160/month

### Recommended Setup

- Azure AD P2 for 20% of users: $900/month
- Azure AD P1 for 80% of users: $2,400/month
- Azure App Service: $55/month
- Supporting services: $25/month
- **Total:** ~$3,380/month

### Enterprise Setup

- Azure AD P2 for 30% of users: $1,350/month
- Azure AD P1 for 70% of users: $2,100/month
- Premium App Service: $150/month
- Full monitoring stack: $100/month
- **Total:** ~$3,700/month

## Summary

**Key Takeaways:**
1. Biggest cost is Azure AD licensing (~95% of total)
2. Infrastructure costs are minimal ($50-300/month)
3. ROI is positive within 3-6 months
4. Security and compliance benefits are significant
5. Cheaper than commercial alternatives

**Next Steps:**
1. Assess your user count and admin count
2. Calculate licensing needs (P1 vs P2)
3. Choose infrastructure deployment model
4. Start with trial period
5. Measure ROI after 90 days
