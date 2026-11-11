"""HTTP controller for departments."""
from app.controllers.resource_controller import ResourceController
from app.services.models.department_service import DepartmentService


class DepartmentController(ResourceController):
    SERVICE_CLASS = DepartmentService