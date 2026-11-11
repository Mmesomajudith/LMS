"""HTTP controller for marks."""
from app.controllers.resource_controller import ResourceController
from app.services.models.mark_service import MarkService


class MarkController(ResourceController):
    SERVICE_CLASS = MarkService