"""Service operations for courses."""
from app.services.resource_service import ResourceService


class CourseService(ResourceService):
    RESOURCE = "courses"