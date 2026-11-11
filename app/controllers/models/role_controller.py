"""HTTP controller for roles."""
from app.controllers.resource_controller import ResourceController
from app.services.models.role_service import RoleService


class RoleController(ResourceController):
    SERVICE_CLASS = RoleService