"""Routes for departments."""
from app.controllers.models.department_controller import DepartmentController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("departments", DepartmentController)