"""HTTP controller for diagnostic sessions."""
from app.controllers.resource_controller import ResourceController
from app.services.models.diagnostic_session_service import DiagnosticSessionService


class DiagnosticSessionController(ResourceController):
    SERVICE_CLASS = DiagnosticSessionService