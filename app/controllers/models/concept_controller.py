"""HTTP controller for concepts."""
from app.controllers.resource_controller import ResourceController
from app.services.models.concept_service import ConceptService


class ConceptController(ResourceController):
    SERVICE_CLASS = ConceptService