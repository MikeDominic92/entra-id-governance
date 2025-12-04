"""
FastAPI Main Application
REST API for Entra ID Governance toolkit
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..config import settings
from .routes import policies, pim, reports, splunk

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.app.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Entra ID Governance API",
    description="REST API for Microsoft Entra ID Governance automation and analysis with Splunk SIEM integration",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    policies.router, prefix="/api/v1/policies", tags=["Conditional Access"]
)
app.include_router(
    pim.router, prefix="/api/v1/pim", tags=["Privileged Identity Management"]
)
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
# v1.1 Enhancement - December 2025: Splunk SIEM Integration
app.include_router(splunk.router, prefix="/api/v1/splunk", tags=["Splunk SIEM"])


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Entra ID Governance API",
        "version": "1.1.0",
        "description": "Microsoft Entra ID Governance automation and analysis with Splunk SIEM integration",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "conditional_access": "/api/v1/policies",
            "pim": "/api/v1/pim",
            "reports": "/api/v1/reports",
            "splunk": "/api/v1/splunk",  # v1.1 Enhancement
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Validate configuration
        is_valid = settings.validate()

        return {
            "status": "healthy" if is_valid else "unhealthy",
            "configuration": "valid" if is_valid else "invalid",
            "timestamp": "2025-11-30T00:00:00Z",
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.app.api_host,
        port=settings.app.api_port,
        log_level=settings.app.log_level.lower(),
    )
