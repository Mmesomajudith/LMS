"""Routes for user roles."""
from app.controllers.models.user_role_controller import UserRoleController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("user_roles", UserRoleController)