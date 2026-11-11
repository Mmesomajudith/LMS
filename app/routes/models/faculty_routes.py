"""Routes for faculties."""
from app.controllers.models.faculty_controller import FacultyController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("faculties", FacultyController)