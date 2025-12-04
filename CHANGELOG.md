# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-tenant support
- Historical trend analysis
- Teams webhook notifications
- Microsoft Sentinel integration
- Additional SIEM connectors (QRadar, ArcSight)

## [1.1.0] - 2025-12-04

### Added - Splunk SIEM Integration

**Major Enhancement**: Enterprise-grade SIEM integration for identity governance event correlation and automated remediation.

#### New Integrations Module (`src/integrations/`)

- **SplunkHECConnector** (`splunk_connector.py`)
  - HTTP Event Collector (HEC) client implementation
  - Secure token-based authentication
  - Batch event submission with newline-delimited JSON
  - Automatic retry with exponential backoff (configurable max retries)
  - SSL certificate verification
  - Mock mode for demonstrations and testing
  - Connection health checks
  - Event statistics tracking (sent, failed, bytes transferred)

- **EventForwarder** (`event_forwarder.py`)
  - Forward identity governance events to Splunk in CIM format
  - Splunk Common Information Model (CIM) data model mapping:
    - Identity Management data model
    - Change data model
    - Authentication data model
    - Risk data model
  - Event types supported:
    - Access review events (pending, approved, denied, completed)
    - PIM role activation events with risk scoring
    - Conditional Access policy changes (created, modified, deleted, enabled, disabled)
    - Entitlement management changes (granted, revoked, modified)
    - Compliance violation detection
  - Automatic severity calculation based on context
  - Batch event forwarding capability
  - Event forwarding statistics

- **AlertReceiver** (`alert_receiver.py`)
  - Webhook endpoint for Splunk correlation alerts
  - Pydantic models for alert validation
  - Enhanced correlation score calculation:
    - Alert severity weighting
    - Event frequency analysis
    - Time window analysis
    - Privileged user detection
  - Automated remediation workflow triggering
  - Alert deduplication with TTL-based caching
  - Category-based alert routing
  - Alert history tracking
  - Remediation handler registration system

#### Configuration Updates

- **New `SplunkConfig` class** in `config.py`:
  - HEC URL, token, index, source, sourcetype configuration
  - SSL verification and timeout settings
  - Feature flags: enabled, mock_mode, auto_remediation
  - Granular event forwarding controls per event type
  - Environment variable support for all settings

#### REST API Enhancements

- **New Splunk API routes** (`/api/v1/splunk/`):
  - `GET /health` - Integration health check and connectivity test
  - `GET /config` - Get sanitized configuration (no secrets)
  - `GET /statistics` - Connector, forwarder, and receiver statistics
  - `POST /events/forward` - Manually forward events to Splunk
  - `POST /alerts/webhook` - Receive Splunk correlation alerts
  - `GET /alerts/history` - Query alert reception history
  - `POST /test/send-event` - Send test event for connectivity validation

- **Updated FastAPI application**:
  - Version bumped to 1.1.0
  - Splunk router integration
  - Updated API documentation

#### Dependencies

- Added `splunk-sdk>=1.7.0` for Splunk HEC support

#### Documentation

- **README.md updates**:
  - New "Splunk SIEM Integration (v1.1 - NEW!)" feature section
  - Splunk configuration examples with environment variables
  - API endpoint documentation
  - Updated roadmap with completed v1.1 and planned v1.2

- **CHANGELOG.md**: Comprehensive v1.1 release notes

### Features Highlights

- **CIM Compliance**: All forwarded events conform to Splunk Common Information Model for seamless Enterprise Security integration
- **Risk Scoring**: Automatic risk score calculation for PIM activations and policy changes
- **Correlation Support**: Enhanced correlation score calculation for multi-event patterns
- **Demo Mode**: Mock mode enables demonstrations without actual Splunk infrastructure
- **Production Ready**: Retry logic, error handling, SSL verification, and statistics tracking

### Breaking Changes

- None - v1.1 is fully backward compatible with v0.1.0

### Known Limitations

- Alert remediation handlers must be registered programmatically
- Alert history is in-memory (persistent storage planned for v1.2)
- Single Splunk instance support (multi-instance planned for v1.2)

### Upgrade Notes

1. Update `.env` with Splunk configuration variables
2. Run `pip install -r requirements.txt` to install `splunk-sdk`
3. Configure Splunk HEC endpoint and generate HEC token
4. Set `SPLUNK_ENABLED=true` to activate integration
5. Use `SPLUNK_MOCK_MODE=true` for testing without Splunk

### Security Considerations

- Store HEC tokens securely (use secrets management in production)
- Enable SSL verification in production environments
- Review auto-remediation handlers before enabling
- Monitor Splunk integration statistics for anomalies

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
