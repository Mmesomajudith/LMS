"""HTTP controller for material section concepts."""
from app.controllers.resource_controller import ResourceController
from app.services.models.material_section_concept_service import MaterialSectionConceptService


class MaterialSectionConceptController(ResourceController):
    SERVICE_CLASS = MaterialSectionConceptService