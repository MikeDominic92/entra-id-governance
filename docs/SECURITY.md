# Security Guidelines

Security best practices for deploying and operating the Entra ID Governance Toolkit.

## Credential Management

### Azure App Registration

**Client Secret Rotation:**
- Rotate secrets every 90-180 days
- Set calendar reminders before expiration
- Use multiple secrets during rotation for zero-downtime

**Storage:**
- Never commit secrets to version control
- Use environment variables or Azure Key Vault
- Restrict `.env` file permissions (Unix: `chmod 600 .env`)

**Monitoring:**
- Enable audit logging for app registration
- Monitor for unauthorized secret changes
- Alert on failed authentication attempts

### Break Glass Accounts

Always exclude emergency admin accounts from:
- Conditional Access policies
- MFA requirements
- Location restrictions

**Break Glass Account Setup:**
```python
# Example: Exclude break glass account from CA policy
from src.automation import PolicyEnforcer

enforcer = PolicyEnforcer()
enforcer.add_exclusion_to_policy(
    policy_id="your-policy-id",
    exclude_users=["breakglass@yourdomain.com"]
)
```

## API Security

### Authentication

**MSAL Token Caching:**
- Token cache file (`.token_cache.json`) contains sensitive data
- Add to .gitignore
- Encrypt if storing on shared systems
- Clear cache when secret is rotated

**Token Expiration:**
- Tokens expire after 1 hour by default
- Client automatically refreshes expired tokens
- Implement proper retry logic (already included)

### Rate Limiting

**Microsoft Graph Limits:**
- 2,000 requests per second per app
- 10,000 requests per 10 minutes per user
- This toolkit implements exponential backoff

**Best Practices:**
- Use batch requests when possible (up to 20 at once)
- Implement caching for frequently accessed data
- Respect Retry-After headers (automatically handled)

### Input Validation

**User Input:**
Always validate user input before passing to Graph API:
```python
# Bad
policy_id = user_input  # Dangerous!
client.get(f"policies/{policy_id}")

# Good
import re
if re.match(r'^[a-f0-9-]{36}$', user_input):
    client.get(f"policies/{user_input}")
else:
    raise ValueError("Invalid policy ID format")
```

## Deployment Security

### Development vs Production

**Development:**
- Use separate tenant for testing
- Lower permission scope when possible
- Enable debug logging
- Report-only CA policies

**Production:**
- Use managed identities when deployed to Azure
- Restrict network access
- Enable minimal logging (INFO level)
- Monitor API usage

### Azure Deployment

**Managed Identity (Recommended):**
```python
# When running on Azure VM/App Service
from azure.identity import DefaultAzureCredential

# Use managed identity instead of client secret
credential = DefaultAzureCredential()
```

**Azure Key Vault:**
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://yourvault.vault.azure.net/", credential=credential)

# Retrieve secrets from Key Vault
client_secret = client.get_secret("entra-governance-secret").value
```

### Network Security

**Restrict Access:**
- Use Azure Private Endpoints for Key Vault
- Implement IP whitelisting for API
- Use VPN/ExpressRoute for on-premises access

**TLS/SSL:**
- Always use HTTPS (enforced by Graph API)
- Verify SSL certificates
- Don't disable certificate verification

## Operational Security

### Logging and Monitoring

**What to Log:**
- Authentication events (success/failure)
- API calls and responses (sanitize secrets!)
- Policy changes
- PIM activations
- Access review decisions

**What NOT to Log:**
- Client secrets
- Access tokens
- Full PII (redact when logging)
- Sensitive user data

**Example Safe Logging:**
```python
import logging

logger = logging.getLogger(__name__)

# Bad - logs sensitive data
logger.info(f"Token: {access_token}")

# Good - logs only necessary info
logger.info(f"Successfully authenticated for tenant {tenant_id}")
```

### Audit Trail

**Azure AD Audit Logs:**
Monitor for:
- New app registrations
- Permission grants
- Secret rotations
- Policy changes
- PIM activations

**Application Logs:**
Store logs in centralized system:
- Azure Log Analytics
- Splunk
- ELK Stack

### Incident Response

**If Secrets are Compromised:**
1. Immediately revoke/rotate client secret
2. Review audit logs for unauthorized activity
3. Check for policy changes
4. Review PIM activations
5. Notify security team
6. Update incident response documentation

**If Policy Changes are Malicious:**
1. Disable/delete malicious policies immediately
2. Restore from backup/known good state
3. Review who made changes (audit logs)
4. Revoke permissions if needed
5. Investigate scope of impact

## Code Security

### Dependency Management

**Vulnerable Dependencies:**
```bash
# Scan for vulnerabilities
pip install safety
safety check --file requirements.txt

# Scan code for security issues
pip install bandit
bandit -r src/
```

**Keep Updated:**
- Review dependency updates regularly
- Subscribe to security advisories
- Use Dependabot or Renovate

### Secrets in Code

**Never Hard-Code:**
```python
# BAD - Never do this!
client_secret = "your-secret-here"
api_key = "12345-67890"

# GOOD - Use environment variables
import os
client_secret = os.getenv("AZURE_CLIENT_SECRET")

# BEST - Use Azure Key Vault
from azure.keyvault.secrets import SecretClient
client_secret = secret_client.get_secret("client-secret").value
```

### Error Handling

**Don't Leak Sensitive Info:**
```python
# Bad - exposes internal details
try:
    client.get("users")
except Exception as e:
    return {"error": str(e)}  # May contain secrets!

# Good - generic error
try:
    client.get("users")
except Exception as e:
    logger.error(f"API call failed: {e}")
    return {"error": "An error occurred. Check logs for details."}
```

## Compliance Considerations

### Data Privacy

**GDPR:**
- Don't store PII unnecessarily
- Implement data retention policies
- Provide data export capabilities
- Honor deletion requests

**Audit Reports:**
- Redact user emails/names when sharing
- Use user IDs instead of names where possible
- Implement access controls on reports

### Regulatory Requirements

**SOC 2:**
- Implement audit logging
- Encrypt data in transit (TLS) and at rest
- Access control and segregation of duties
- Regular security reviews

**ISO 27001:**
- Asset management (track all secrets/credentials)
- Access control procedures
- Cryptographic controls
- Incident management

## Security Checklist

Before deploying to production:

- [ ] Client secrets stored in Key Vault (not .env)
- [ ] Break glass accounts excluded from CA policies
- [ ] Audit logging enabled
- [ ] Rate limiting implemented
- [ ] Input validation on all user inputs
- [ ] Error messages don't leak sensitive data
- [ ] .env file in .gitignore
- [ ] Dependency vulnerabilities scanned
- [ ] RBAC implemented (least privilege)
- [ ] Incident response plan documented
- [ ] Regular secret rotation scheduled
- [ ] Monitoring alerts configured
- [ ] Backup/restore procedures tested
- [ ] Security training for operators
- [ ] Penetration testing completed

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. Email security@yourdomain.com with details
3. Include steps to reproduce
4. Allow 90 days for fix before public disclosure

## Resources

- [Microsoft Security Best Practices](https://learn.microsoft.com/en-us/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Azure Security Baseline](https://learn.microsoft.com/en-us/security/benchmark/azure/)
- [CIS Microsoft 365 Foundations Benchmark](https://www.cisecurity.org/)
