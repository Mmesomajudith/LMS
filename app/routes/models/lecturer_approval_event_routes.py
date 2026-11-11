"""Routes for lecturer approval events."""
from app.controllers.models.lecturer_approval_event_controller import LecturerApprovalEventController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("lecturer_approval_events", LecturerApprovalEventController)