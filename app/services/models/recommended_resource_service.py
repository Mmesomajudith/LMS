"""Service operations for recommended resources."""
from app.services.resource_service import ResourceService


class RecommendedResourceService(ResourceService):
    RESOURCE = "recommended_resources"