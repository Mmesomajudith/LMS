"""Service operations for enrolments."""
from app.services.resource_service import ResourceService


class EnrolmentService(ResourceService):
    RESOURCE = "enrolments"