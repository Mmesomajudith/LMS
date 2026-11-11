"""Service operations for concepts."""
from app.services.resource_service import ResourceService


class ConceptService(ResourceService):
    RESOURCE = "concepts"