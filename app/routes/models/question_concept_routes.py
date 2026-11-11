"""Routes for question concepts."""
from app.controllers.models.question_concept_controller import QuestionConceptController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("question_concepts", QuestionConceptController)