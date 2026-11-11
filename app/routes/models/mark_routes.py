"""Routes for marks."""
from app.controllers.models.mark_controller import MarkController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("marks", MarkController)