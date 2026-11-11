"""HTTP controller for material sections."""
from app.controllers.resource_controller import ResourceController
from app.services.models.material_section_service import MaterialSectionService


class MaterialSectionController(ResourceController):
    SERVICE_CLASS = MaterialSectionService