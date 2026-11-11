"""HTTP controller for question concepts."""
from app.controllers.resource_controller import ResourceController
from app.services.models.question_concept_service import QuestionConceptService


class QuestionConceptController(ResourceController):
    SERVICE_CLASS = QuestionConceptService