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

    def validate(self) -> bool:
        """Validate all configurations"""
        try:
            _ = self.graph
            _ = self.app
            return True
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False


# Global settings instance
settings = Settings()
