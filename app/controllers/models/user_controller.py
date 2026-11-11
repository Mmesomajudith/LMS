"""HTTP controller for users."""
from app.controllers.resource_controller import ResourceController
from app.services.models.user_service import UserService


class UserController(ResourceController):
    SERVICE_CLASS = UserService