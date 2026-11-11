"""Service operations for assignment questions."""
from app.services.resource_service import ResourceService


class AssignmentQuestionService(ResourceService):
    RESOURCE = "assignment_questions"