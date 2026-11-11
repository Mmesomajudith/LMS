"""HTTP controller for submissions."""
from app.controllers.resource_controller import ResourceController
from app.services.models.submission_service import SubmissionService


class SubmissionController(ResourceController):
    SERVICE_CLASS = SubmissionService