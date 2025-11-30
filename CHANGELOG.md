# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-tenant support
- React dashboard frontend
- Historical trend analysis
- Teams webhook notifications

## [0.1.0] - 2025-11-30

### Added
- Initial release
- Conditional Access policy analysis
- PIM role assignment analysis and automation
- Access Review monitoring and automation
- Entitlement Management analysis
- Microsoft Graph API client with retry logic
- FastAPI REST interface
- PowerShell scripts for AD admins
- Comprehensive compliance reporting
- Risk assessment reporting
- Governance dashboard data provider
- Unit tests with pytest
- Full documentation

### Features
- **Analyzers**
  - Conditional Access coverage analysis
  - Policy conflict detection
  - Security scoring (0-100)
  - PIM standing access violation detection
  - Excessive privilege checks
  - Access Review completion tracking
  - Entitlement package analysis

- **Automation**
  - PIM role activation/deactivation
  - Bulk approval workflows
  - Policy enforcement
  - Scheduled activations

- **Reporting**
  - Full compliance reports
  - Risk assessments
  - Dashboard KPIs
  - CSV/JSON export

- **API**
  - RESTful endpoints
  - Interactive Swagger docs
  - Health checks

- **PowerShell**
  - Get-ConditionalAccessPolicies.ps1
  - Export-PIMAssignments.ps1
  - Start-AccessReview.ps1
  - Set-ConditionalAccessPolicy.ps1

### Security
- MSAL token caching
- Secure credential management
- Retry with exponential backoff
- Rate limit handling

## Release Notes

### v0.1.0 - Initial Public Release

This is the first public release of the Entra ID Governance Toolkit. It provides a comprehensive set of tools for analyzing and automating Microsoft Entra ID governance tasks.

**Key Highlights:**
- Production-ready Graph API client
- Complete analyzer suite
- REST API with 15+ endpoints
- PowerShell scripts for traditional admins
- Full test coverage
- Comprehensive documentation

**Known Limitations:**
- Single tenant support only
- No historical data storage
- Limited dashboard visualizations

**Upgrade Notes:**
- First release, no upgrade path yet

**Breaking Changes:**
- None (initial release)
