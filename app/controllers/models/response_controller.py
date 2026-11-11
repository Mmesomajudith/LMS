"""HTTP controller for responses."""
from app.controllers.resource_controller import ResourceController
from app.services.models.response_service import ResponseService


class ResponseController(ResourceController):
    SERVICE_CLASS = ResponseService