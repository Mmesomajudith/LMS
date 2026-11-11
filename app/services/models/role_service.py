"""Service operations for roles."""
from app.services.resource_service import ResourceService


class RoleService(ResourceService):
    RESOURCE = "roles"