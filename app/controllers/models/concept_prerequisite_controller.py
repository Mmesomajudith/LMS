"""HTTP controller for concept prerequisites."""
from app.controllers.resource_controller import ResourceController
from app.services.models.concept_prerequisite_service import ConceptPrerequisiteService


class ConceptPrerequisiteController(ResourceController):
    SERVICE_CLASS = ConceptPrerequisiteService