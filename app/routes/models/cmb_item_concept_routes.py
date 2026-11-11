"""Routes for CMB item concepts."""
from app.controllers.models.cmb_item_concept_controller import CMBItemConceptController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("cmb_item_concepts", CMBItemConceptController)