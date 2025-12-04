"""
Configuration management for Entra ID Governance toolkit
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GraphAPIConfig(BaseModel):
    """Microsoft Graph API configuration"""

    tenant_id: str = Field(..., description="Azure AD Tenant ID")
    client_id: str = Field(..., description="Azure App Registration Client ID")
    client_secret: str = Field(..., description="Azure App Registration Client Secret")
    authority: str = Field(
        default="https://login.microsoftonline.com",
        description="Azure AD authority URL",
    )
    scopes: list[str] = Field(
        default=["https://graph.microsoft.com/.default"], description="Graph API scopes"
    )

    @validator("tenant_id", "client_id", "client_secret")
    def validate_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Configuration value cannot be empty")
        return v

    @property
    def authority_url(self) -> str:
        """Get full authority URL with tenant"""
        return f"{self.authority}/{self.tenant_id}"


class SplunkConfig(BaseModel):
    """
    Splunk SIEM integration configuration
    v1.1 Enhancement - December 2025
    """

    # HEC Configuration
    hec_url: str = Field(
        default="https://splunk.example.com:8088",
        description="Splunk HEC endpoint URL",
    )
    hec_token: str = Field(default="", description="HEC authentication token")
    index: str = Field(default="entra_id_governance", description="Target Splunk index")
    source: str = Field(
        default="entra_governance_toolkit", description="Event source identifier"
    )
    sourcetype: str = Field(
        default="entra:identity:governance", description="Splunk sourcetype"
    )

    # Connection settings
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    timeout: int = Field(default=30, description="HTTP timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")

    # Feature flags
    enabled: bool = Field(default=False, description="Enable Splunk integration")
    mock_mode: bool = Field(
        default=False, description="Mock mode for demos (no actual API calls)"
    )
    auto_remediation: bool = Field(
        default=False, description="Enable automatic remediation from alerts"
    )

    # Event forwarding
    forward_access_reviews: bool = Field(
        default=True, description="Forward access review events"
    )
    forward_pim_activations: bool = Field(
        default=True, description="Forward PIM activation events"
    )
    forward_policy_changes: bool = Field(
        default=True, description="Forward policy change events"
    )
    forward_compliance_violations: bool = Field(
        default=True, description="Forward compliance violation events"
    )

    @validator("hec_token")
    def validate_token(cls, v, values):
        """Validate HEC token is provided if Splunk is enabled"""
        if (
            values.get("enabled", False)
            and not values.get("mock_mode", False)
            and not v
        ):
            raise ValueError("HEC token is required when Splunk integration is enabled")
        return v


class AppConfig(BaseModel):
    """Application configuration"""

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_debug: bool = Field(default=False, description="Debug mode")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(
        default="entra_governance.log", description="Log file path"
    )

    # Cache settings
    token_cache_file: str = Field(
        default=".token_cache.json", description="Token cache file"
    )
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")

    # Rate limiting
    max_retries: int = Field(default=3, description="Maximum API retry attempts")
    retry_delay: int = Field(default=2, description="Delay between retries in seconds")
    batch_size: int = Field(default=20, description="Batch request size")

    # Reporting
    report_output_dir: str = Field(
        default="reports", description="Output directory for reports"
    )

    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()


class Settings:
    """Global settings manager"""

    def __init__(self):
        self._graph_config: Optional[GraphAPIConfig] = None
        self._app_config: Optional[AppConfig] = None
        self._splunk_config: Optional[SplunkConfig] = None

    @property
    def graph(self) -> GraphAPIConfig:
        """Get Graph API configuration"""
        if self._graph_config is None:
            self._graph_config = GraphAPIConfig(
                tenant_id=os.getenv("AZURE_TENANT_ID", ""),
                client_id=os.getenv("AZURE_CLIENT_ID", ""),
                client_secret=os.getenv("AZURE_CLIENT_SECRET", ""),
            )
        return self._graph_config

    @property
    def app(self) -> AppConfig:
        """Get application configuration"""
        if self._app_config is None:
            self._app_config = AppConfig(
                api_host=os.getenv("API_HOST", "0.0.0.0"),
                api_port=int(os.getenv("API_PORT", "8000")),
                api_debug=os.getenv("API_DEBUG", "false").lower() == "true",
                log_level=os.getenv("LOG_LEVEL", "INFO"),
                log_file=os.getenv("LOG_FILE", "entra_governance.log"),
            )
        return self._app_config

    @property
    def splunk(self) -> SplunkConfig:
        """
        Get Splunk SIEM configuration
        v1.1 Enhancement - December 2025
        """
        if self._splunk_config is None:
            self._splunk_config = SplunkConfig(
                hec_url=os.getenv("SPLUNK_HEC_URL", "https://splunk.example.com:8088"),
                hec_token=os.getenv("SPLUNK_HEC_TOKEN", ""),
                index=os.getenv("SPLUNK_INDEX", "entra_id_governance"),
                source=os.getenv("SPLUNK_SOURCE", "entra_governance_toolkit"),
                sourcetype=os.getenv("SPLUNK_SOURCETYPE", "entra:identity:governance"),
                verify_ssl=os.getenv("SPLUNK_VERIFY_SSL", "true").lower() == "true",
                timeout=int(os.getenv("SPLUNK_TIMEOUT", "30")),
                max_retries=int(os.getenv("SPLUNK_MAX_RETRIES", "3")),
                enabled=os.getenv("SPLUNK_ENABLED", "false").lower() == "true",
                mock_mode=os.getenv("SPLUNK_MOCK_MODE", "false").lower() == "true",
                auto_remediation=os.getenv("SPLUNK_AUTO_REMEDIATION", "false").lower()
                == "true",
                forward_access_reviews=os.getenv(
                    "SPLUNK_FORWARD_ACCESS_REVIEWS", "true"
                ).lower()
                == "true",
                forward_pim_activations=os.getenv(
                    "SPLUNK_FORWARD_PIM_ACTIVATIONS", "true"
                ).lower()
                == "true",
                forward_policy_changes=os.getenv(
                    "SPLUNK_FORWARD_POLICY_CHANGES", "true"
                ).lower()
                == "true",
                forward_compliance_violations=os.getenv(
                    "SPLUNK_FORWARD_COMPLIANCE_VIOLATIONS", "true"
                ).lower()
                == "true",
            )
        return self._splunk_config

    def validate(self) -> bool:
        """Validate all configurations"""
        try:
            _ = self.graph
            _ = self.app
            _ = self.splunk
            return True
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create global settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# For backwards compatibility
settings = get_settings()
