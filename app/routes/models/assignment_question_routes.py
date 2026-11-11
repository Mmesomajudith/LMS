"""Routes for assignment questions."""
from app.controllers.models.assignment_question_controller import AssignmentQuestionController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("assignment_questions", AssignmentQuestionController)