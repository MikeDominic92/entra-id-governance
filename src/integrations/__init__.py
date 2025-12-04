"""
Splunk SIEM Integration Module for Entra ID Governance
v1.1 Enhancement - December 2025

This module provides comprehensive Splunk integration capabilities including:
- HTTP Event Collector (HEC) connectivity
- Event forwarding for identity governance events
- Alert reception via webhooks
- CIM format mapping for Splunk Enterprise Security
"""

from .splunk_connector import SplunkHECConnector
from .event_forwarder import EventForwarder
from .alert_receiver import AlertReceiver

__all__ = [
    "SplunkHECConnector",
    "EventForwarder",
    "AlertReceiver",
]

__version__ = "1.1.0"
