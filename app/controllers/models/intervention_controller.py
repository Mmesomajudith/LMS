"""HTTP controller for interventions."""
from app.controllers.resource_controller import ResourceController
from app.services.models.intervention_service import InterventionService


class InterventionController(ResourceController):
    SERVICE_CLASS = InterventionService