"""Routes for assignments."""
from app.controllers.models.assignment_controller import AssignmentController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("assignments", AssignmentController)