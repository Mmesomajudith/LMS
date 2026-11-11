"""HTTP controller for user roles."""
from app.controllers.resource_controller import ResourceController
from app.services.models.user_role_service import UserRoleService


class UserRoleController(ResourceController):
    SERVICE_CLASS = UserRoleService