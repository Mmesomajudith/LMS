"""HTTP controller for faculties."""
from app.controllers.resource_controller import ResourceController
from app.services.models.faculty_service import FacultyService


class FacultyController(ResourceController):
    SERVICE_CLASS = FacultyService