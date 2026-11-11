"""Routes for interventions."""
from app.controllers.models.intervention_controller import InterventionController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("interventions", InterventionController)