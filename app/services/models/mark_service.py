"""Service operations for marks."""
from app.services.resource_service import ResourceService


class MarkService(ResourceService):
    RESOURCE = "marks"