"""Service operations for AI gateway requests."""
from app.services.resource_service import ResourceService


class AIGatewayRequestService(ResourceService):
    RESOURCE = "ai_gateway_requests"