"""Routes for material section concepts."""
from app.controllers.models.material_section_concept_controller import MaterialSectionConceptController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("material_section_concepts", MaterialSectionConceptController)