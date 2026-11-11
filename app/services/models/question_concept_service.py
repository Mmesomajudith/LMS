"""Service operations for question concepts."""
from app.services.resource_service import ResourceService


class QuestionConceptService(ResourceService):
    RESOURCE = "question_concepts"