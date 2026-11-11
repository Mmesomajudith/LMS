"""HTTP controller for enrolments."""
from app.controllers.resource_controller import ResourceController
from app.services.models.enrolment_service import EnrolmentService


class EnrolmentController(ResourceController):
    SERVICE_CLASS = EnrolmentService