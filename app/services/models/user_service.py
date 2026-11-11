"""Service operations for users."""
from app.services.resource_service import ResourceService


class UserService(ResourceService):
    RESOURCE = "users"