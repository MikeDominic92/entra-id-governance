"""
Reports API Routes
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

from ...reports import ComplianceReporter, RiskReporter, GovernanceDashboard

router = APIRouter()


@router.get("/compliance")
async def get_compliance_report():
    """Generate full compliance report"""
    try:
        reporter = ComplianceReporter()
        report = reporter.generate_full_compliance_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compliance/export")
async def export_compliance_report(format: str = "json"):
    """Export compliance report to file"""
    try:
        reporter = ComplianceReporter()
        report = reporter.generate_full_compliance_report()

        if format.lower() == "json":
            filepath = reporter.save_report_to_file(report)
        elif format.lower() == "csv":
            filepath = reporter.export_to_csv(report)
        else:
            raise HTTPException(
                status_code=400, detail="Invalid format. Use 'json' or 'csv'"
            )

        return FileResponse(
            path=filepath,
            filename=filepath.split("\\")[-1],
            media_type="application/octet-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk")
async def get_risk_report():
    """Generate risk assessment report"""
    try:
        reporter = RiskReporter()
        report = reporter.generate_risk_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_data():
    """Get full dashboard data"""
    try:
        dashboard = GovernanceDashboard()
        data = dashboard.get_dashboard_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/widget/{widget_type}")
async def get_widget_data(widget_type: str):
    """Get specific widget data"""
    try:
        dashboard = GovernanceDashboard()
        data = dashboard.get_widget_data(widget_type)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
