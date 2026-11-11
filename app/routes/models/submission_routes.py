"""Routes for submissions."""
from app.controllers.models.submission_controller import SubmissionController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("submissions", SubmissionController)