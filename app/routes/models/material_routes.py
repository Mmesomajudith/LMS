"""Routes for materials."""
from app.controllers.models.material_controller import MaterialController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("materials", MaterialController)