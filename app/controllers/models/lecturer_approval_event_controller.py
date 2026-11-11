"""HTTP controller for lecturer approval events."""
from app.controllers.resource_controller import ResourceController
from app.services.models.lecturer_approval_event_service import LecturerApprovalEventService


class LecturerApprovalEventController(ResourceController):
    SERVICE_CLASS = LecturerApprovalEventService