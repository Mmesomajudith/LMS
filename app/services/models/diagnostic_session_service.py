"""Service operations for diagnostic sessions."""
from app.services.resource_service import ResourceService


class DiagnosticSessionService(ResourceService):
    RESOURCE = "diagnostic_sessions"