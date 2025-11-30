# ADR-001: Use Microsoft Graph API for All Entra ID Operations

**Status:** Accepted

**Date:** 2025-11-30

**Deciders:** MikeDominic92

## Context

We need to interact with Microsoft Entra ID (Azure AD) to:
- Analyze Conditional Access policies
- Manage PIM role assignments
- Automate Access Reviews
- Generate compliance reports

Multiple approaches exist for interacting with Entra ID:
1. Microsoft Graph API (REST)
2. Azure AD PowerShell module
3. Microsoft Graph PowerShell SDK
4. Azure CLI

## Decision

We will use **Microsoft Graph API** as the primary interface for all Entra ID operations, implemented via MSAL (Microsoft Authentication Library) and httpx for HTTP requests.

## Rationale

### Advantages of Microsoft Graph API

**1. Future-Proof**
- Microsoft is consolidating all APIs into Graph
- Azure AD Graph is deprecated (June 2023)
- New features only available in Graph API
- Long-term Microsoft investment

**2. Language Agnostic**
- RESTful HTTP interface
- Works from Python, JavaScript, PowerShell, etc.
- Easier to integrate with other systems
- Standard HTTP tools and debugging

**3. Comprehensive Coverage**
- Single API for all Microsoft 365 services
- Consistent patterns across endpoints
- Beta endpoint for preview features
- Extensive documentation

**4. Better Performance**
- Native HTTP/JSON
- Batch request support (20 requests at once)
- Delta queries for incremental changes
- Efficient pagination

**5. Authentication Flexibility**
- Service principal (app-only)
- Delegated user permissions
- Managed identity support
- Certificate-based auth

### Why Not Alternatives?

**Azure AD PowerShell:**
- Deprecated, replaced by Graph PowerShell
- Limited functionality
- PowerShell dependency
- Not cross-platform friendly

**Microsoft Graph PowerShell SDK:**
- Great for PowerShell users
- But adds PowerShell dependency for Python toolkit
- Wrapper around Graph API anyway
- Harder to debug

**Azure CLI:**
- Not all Graph operations supported
- Primarily for Azure Resource Manager
- Less granular control
- Awkward error handling

## Implementation

### MSAL for Authentication

Using `msal` Python library for token acquisition:
- Handles OAuth 2.0 flows
- Automatic token caching
- Token refresh
- Industry standard

### httpx for HTTP Requests

Using `httpx` instead of `requests`:
- Async support (future enhancement)
- HTTP/2 support
- Better timeout handling
- More modern API

### Retry Logic

Implement exponential backoff for:
- Rate limiting (429 responses)
- Transient failures (5xx errors)
- Token expiration (401)

### Batch Requests

Use `$batch` endpoint when possible:
- Reduce round trips
- Better performance
- Atomic operations

## Consequences

### Positive

- Future-proof architecture
- Consistent API patterns
- Cross-platform compatibility
- Well-documented
- Community support
- Easy to test/mock

### Negative

- Learning curve for Graph API specifics
- Must handle pagination manually
- Rate limiting considerations
- Permission model can be complex

### Neutral

- Requires Azure App Registration
- Admin consent needed for app permissions
- API versioning (v1.0 vs beta)

## Alternatives Considered

### 1. Azure AD PowerShell

**Pros:**
- Familiar to AD admins
- Simple cmdlet interface

**Cons:**
- Deprecated by Microsoft
- PowerShell dependency
- Limited future support

**Rejected because:** Deprecated technology

### 2. Microsoft Graph PowerShell SDK

**Pros:**
- Official Microsoft SDK
- Active development
- Good for PowerShell users

**Cons:**
- PowerShell dependency in Python project
- Wrapper complexity
- Harder debugging

**Rejected because:** Adds unnecessary dependency layer

### 3. Azure CLI

**Pros:**
- Cross-platform
- Good for scripting

**Cons:**
- Limited Graph API coverage
- Primarily ARM-focused
- Not designed for this use case

**Rejected because:** Limited functionality for identity management

## Validation

Success criteria:
- ✅ Can authenticate with service principal
- ✅ Can retrieve Conditional Access policies
- ✅ Can read PIM assignments
- ✅ Can manage Access Reviews
- ✅ Handles rate limiting gracefully
- ✅ Token caching works
- ✅ Batch requests supported

## References

- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/)
- [MSAL Python Documentation](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-overview)
- [Azure AD Graph Deprecation](https://learn.microsoft.com/en-us/graph/migrate-azure-ad-graph-overview)

## Notes

PowerShell scripts are included as supplementary tools for administrators who prefer PowerShell, but they also use Microsoft Graph PowerShell SDK which calls Graph API under the hood.

## Review

This ADR should be reviewed if:
- Microsoft deprecates Graph API (unlikely)
- A new official Python SDK is released
- Authentication patterns change significantly
