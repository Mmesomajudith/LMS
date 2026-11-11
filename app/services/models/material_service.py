"""Service operations for materials."""
from app.services.resource_service import ResourceService


class MaterialService(ResourceService):
    RESOURCE = "materials"