"""Routes for diagnostic sessions."""
from app.controllers.models.diagnostic_session_controller import DiagnosticSessionController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("diagnostic_sessions", DiagnosticSessionController)