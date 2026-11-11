"""Routes for concepts."""
from app.controllers.models.concept_controller import ConceptController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("concepts", ConceptController)