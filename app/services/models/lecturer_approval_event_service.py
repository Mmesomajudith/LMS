"""Service operations for lecturer approval events."""
from app.services.resource_service import ResourceService


class LecturerApprovalEventService(ResourceService):
    RESOURCE = "lecturer_approval_events"