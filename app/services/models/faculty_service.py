"""Service operations for faculties."""
from app.services.resource_service import ResourceService


class FacultyService(ResourceService):
    RESOURCE = "faculties"