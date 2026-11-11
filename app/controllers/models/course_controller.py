"""HTTP controller for courses."""
from app.controllers.resource_controller import ResourceController
from app.services.models.course_service import CourseService


class CourseController(ResourceController):
    SERVICE_CLASS = CourseService