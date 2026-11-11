"""Routes for roles."""
from app.controllers.models.role_controller import RoleController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("roles", RoleController)