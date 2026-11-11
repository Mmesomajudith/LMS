"""Routes for candidate explanations."""
from app.controllers.models.candidate_explanation_controller import CandidateExplanationController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("candidate_explanations", CandidateExplanationController)