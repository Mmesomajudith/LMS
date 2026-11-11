"""Routes for recommended resources."""
from app.controllers.models.recommended_resource_controller import RecommendedResourceController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("recommended_resources", RecommendedResourceController)