"""Service operations for material sections."""
from app.services.resource_service import ResourceService


class MaterialSectionService(ResourceService):
    RESOURCE = "material_sections"