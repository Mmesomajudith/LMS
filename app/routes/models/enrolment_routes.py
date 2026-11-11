"""Routes for enrolments."""
from app.controllers.models.enrolment_controller import EnrolmentController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("enrolments", EnrolmentController)