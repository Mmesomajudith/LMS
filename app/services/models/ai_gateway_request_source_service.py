"""Service operations for AI gateway request sources."""
from app.services.resource_service import ResourceService


class AIGatewayRequestSourceService(ResourceService):
    RESOURCE = "ai_gateway_request_sources"