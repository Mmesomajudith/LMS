"""Routes for AI gateway request sources."""
from app.controllers.models.ai_gateway_request_source_controller import AIGatewayRequestSourceController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("ai_gateway_request_sources", AIGatewayRequestSourceController)