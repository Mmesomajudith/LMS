"""Service operations for assignments."""
from app.services.resource_service import ResourceService


class AssignmentService(ResourceService):
    RESOURCE = "assignments"