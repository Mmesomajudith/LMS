"""HTTP controller for assignment questions."""
from app.controllers.resource_controller import ResourceController
from app.services.models.assignment_question_service import AssignmentQuestionService


class AssignmentQuestionController(ResourceController):
    SERVICE_CLASS = AssignmentQuestionService