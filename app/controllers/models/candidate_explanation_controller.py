"""HTTP controller for candidate explanations."""
from app.controllers.resource_controller import ResourceController
from app.services.models.candidate_explanation_service import CandidateExplanationService


class CandidateExplanationController(ResourceController):
    SERVICE_CLASS = CandidateExplanationService