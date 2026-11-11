"""HTTP controller for AI gateway requests."""
from app.controllers.resource_controller import ResourceController
from app.services.models.ai_gateway_request_service import AIGatewayRequestService


class AIGatewayRequestController(ResourceController):
    SERVICE_CLASS = AIGatewayRequestService