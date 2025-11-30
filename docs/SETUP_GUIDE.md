# Setup Guide

This guide walks you through setting up the Entra ID Governance Toolkit from scratch.

## Prerequisites

- Azure AD Premium P2 license (required for PIM and Access Reviews)
- Global Administrator or appropriate delegated permissions
- Python 3.11 or higher
- PowerShell 7.0+ (for PowerShell scripts)
- Git

## Step 1: Azure App Registration

### Create App Registration

1. Sign in to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Configure:
   - **Name:** `Entra-ID-Governance-Toolkit`
   - **Supported account types:** Accounts in this organizational directory only
   - **Redirect URI:** Leave blank (not needed for service principal)
5. Click **Register**

### Note Important Values

After registration, note these values (you'll need them):
- **Application (client) ID**
- **Directory (tenant) ID**

### Create Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **New client secret**
3. Description: `Governance-Toolkit-Secret`
4. Expiration: **180 days** (rotate before expiry)
5. Click **Add**
6. **IMMEDIATELY COPY THE VALUE** (you can't see it again)

### Grant API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph** → **Application permissions**
4. Add the following permissions:

**Required Permissions:**
```
Policy.Read.All
Policy.ReadWrite.ConditionalAccess
RoleManagement.Read.All
RoleManagement.ReadWrite.Directory
AccessReview.Read.All
AccessReview.ReadWrite.All
Directory.Read.All
EntitlementManagement.Read.All
```

5. Click **Add permissions**
6. Click **Grant admin consent for [Your Org]**
7. Confirm by clicking **Yes**

### Verify Permissions

After granting consent, you should see green checkmarks next to all permissions.

## Step 2: Python Environment Setup

### Clone Repository

```bash
git clone https://github.com/MikeDominic92/entra-id-governance.git
cd entra-id-governance
```

### Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Configuration

### Create Environment File

```bash
cp .env.example .env
```

### Edit .env File

Open `.env` in a text editor and add your Azure values:

```env
# Azure AD Configuration
AZURE_TENANT_ID=your-tenant-id-here
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=entra_governance.log
```

**Security Note:** Never commit the `.env` file to version control!

## Step 4: Verify Setup

### Test Graph API Connection

Create a test script `test_connection.py`:

```python
from src.config import settings
from src.graph_client import GraphClient

# Validate configuration
if not settings.validate():
    print("Configuration validation failed!")
    exit(1)

print("Configuration validated successfully!")

# Test Graph API connection
try:
    client = GraphClient()
    policies = client.get_all_pages("identity/conditionalAccess/policies")
    print(f"✓ Successfully connected to Microsoft Graph!")
    print(f"✓ Retrieved {len(policies)} Conditional Access policies")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)
```

Run the test:
```bash
python test_connection.py
```

Expected output:
```
Configuration validated successfully!
✓ Successfully connected to Microsoft Graph!
✓ Retrieved X Conditional Access policies
```

## Step 5: PowerShell Setup (Optional)

### Install Microsoft Graph PowerShell Module

```powershell
# Install the required modules
Install-Module Microsoft.Graph.Authentication -Scope CurrentUser -Force
Install-Module Microsoft.Graph.Identity.SignIns -Scope CurrentUser -Force
Install-Module Microsoft.Graph.Identity.Governance -Scope CurrentUser -Force

# Verify installation
Get-Module Microsoft.Graph.* -ListAvailable
```

### Connect to Microsoft Graph

```powershell
# Connect with required scopes
Connect-MgGraph -Scopes "Policy.Read.All", "RoleManagement.Read.All"

# Verify connection
Get-MgContext
```

## Step 6: Run Your First Analysis

### Conditional Access Analysis

```python
from src.analyzers import ConditionalAccessAnalyzer

analyzer = ConditionalAccessAnalyzer()
coverage = analyzer.analyze_policy_coverage()
print(f"Total policies: {coverage['summary']['total_policies']}")
print(f"Enabled: {coverage['summary']['enabled']}")
```

### PIM Analysis

```python
from src.analyzers import PIMAnalyzer

pim = PIMAnalyzer()
violations = pim.detect_standing_admin_access()
print(f"Standing admin violations: {len(violations)}")
```

### Generate Compliance Report

```python
from src.reports import ComplianceReporter

reporter = ComplianceReporter()
report = reporter.generate_full_compliance_report()
print(f"Compliance Score: {report['compliance_score']}")

# Save to file
filepath = reporter.save_report_to_file(report)
print(f"Report saved to: {filepath}")
```

## Step 7: Start the API (Optional)

### Run FastAPI Server

```bash
# Development mode
python -m src.api.main

# Production mode with uvicorn
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

### Access API Documentation

Open browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Common Issues

#### "Configuration validation failed"

**Cause:** Missing or invalid environment variables

**Solution:**
1. Verify `.env` file exists
2. Check all required values are set
3. Ensure no extra spaces in values

#### "Token acquisition failed: invalid_client"

**Cause:** Incorrect client ID or secret

**Solution:**
1. Verify client ID matches Azure Portal
2. Regenerate client secret if needed
3. Check for copy/paste errors

#### "Insufficient privileges"

**Cause:** API permissions not granted or consent not given

**Solution:**
1. Verify all permissions are added
2. Ensure admin consent was granted (green checkmarks)
3. Wait 5-10 minutes for permissions to propagate

#### "Failed to fetch CA policies"

**Cause:** Tenant doesn't have CA policies or permissions issue

**Solution:**
1. Create at least one CA policy in Azure Portal
2. Verify `Policy.Read.All` permission
3. Check user has appropriate role

## Security Best Practices

1. **Rotate secrets regularly** - Set calendar reminder for 6 months
2. **Use managed identities** when running in Azure
3. **Restrict .env file permissions** - `chmod 600 .env` on Linux
4. **Never commit secrets** - Verify .gitignore includes .env
5. **Use Azure Key Vault** for production deployments
6. **Enable audit logging** in Azure AD
7. **Monitor API usage** via Azure AD sign-in logs

## Next Steps

- Read [ENTRA_ID_CONCEPTS.md](ENTRA_ID_CONCEPTS.md) to understand governance concepts
- Review [SECURITY.md](SECURITY.md) for security guidelines
- Explore the API documentation at `/docs`
- Check out example scripts in `examples/` (if available)

## Getting Help

- Review [README.md](../README.md) for usage examples
- Check [GitHub Issues](https://github.com/MikeDominic92/entra-id-governance/issues)
- Consult [Microsoft Graph API documentation](https://learn.microsoft.com/en-us/graph/)

## Appendix: Permission Details

### Policy.Read.All
Read Conditional Access policies and named locations

### Policy.ReadWrite.ConditionalAccess
Create, update, and delete Conditional Access policies

### RoleManagement.Read.All
Read PIM role assignments and definitions

### RoleManagement.ReadWrite.Directory
Manage PIM role assignments (activate, deactivate)

### AccessReview.Read.All
Read access review definitions and decisions

### AccessReview.ReadWrite.All
Create and manage access reviews

### Directory.Read.All
Read directory objects (users, groups, etc.)

### EntitlementManagement.Read.All
Read entitlement management resources
