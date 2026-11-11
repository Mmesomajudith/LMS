"""Routes for concept prerequisites."""
from app.controllers.models.concept_prerequisite_controller import ConceptPrerequisiteController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("concept_prerequisites", ConceptPrerequisiteController)