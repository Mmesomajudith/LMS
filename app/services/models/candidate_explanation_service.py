"""Service operations for candidate explanations."""
from app.services.resource_service import ResourceService


class CandidateExplanationService(ResourceService):
    RESOURCE = "candidate_explanations"