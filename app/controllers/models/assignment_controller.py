"""HTTP controller for assignments."""
from app.controllers.resource_controller import ResourceController
from app.services.models.assignment_service import AssignmentService


class AssignmentController(ResourceController):
    SERVICE_CLASS = AssignmentService