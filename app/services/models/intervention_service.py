"""Service operations for interventions."""
from app.services.resource_service import ResourceService


class InterventionService(ResourceService):
    RESOURCE = "interventions"