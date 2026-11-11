"""Routes for responses."""
from app.controllers.models.response_controller import ResponseController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("responses", ResponseController)