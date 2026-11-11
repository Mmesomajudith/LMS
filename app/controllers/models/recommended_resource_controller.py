"""HTTP controller for recommended resources."""
from app.controllers.resource_controller import ResourceController
from app.services.models.recommended_resource_service import RecommendedResourceService


class RecommendedResourceController(ResourceController):
    SERVICE_CLASS = RecommendedResourceService