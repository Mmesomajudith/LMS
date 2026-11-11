"""HTTP controller for AI gateway request sources."""
from app.controllers.resource_controller import ResourceController
from app.services.models.ai_gateway_request_source_service import AIGatewayRequestSourceService


class AIGatewayRequestSourceController(ResourceController):
    SERVICE_CLASS = AIGatewayRequestSourceService