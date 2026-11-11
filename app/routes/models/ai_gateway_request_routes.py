"""Routes for AI gateway requests."""
from app.controllers.models.ai_gateway_request_controller import AIGatewayRequestController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("ai_gateway_requests", AIGatewayRequestController)