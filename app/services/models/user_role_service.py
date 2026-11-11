"""Service operations for user roles."""
from app.services.resource_service import ResourceService


class UserRoleService(ResourceService):
    RESOURCE = "user_roles"