"""HTTP controller for materials."""
from app.controllers.resource_controller import ResourceController
from app.services.models.material_service import MaterialService


class MaterialController(ResourceController):
    SERVICE_CLASS = MaterialService