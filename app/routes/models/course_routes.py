"""Routes for courses."""
from app.controllers.models.course_controller import CourseController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("courses", CourseController)