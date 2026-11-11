"""Routes for users."""
from app.controllers.models.user_controller import UserController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("users", UserController)