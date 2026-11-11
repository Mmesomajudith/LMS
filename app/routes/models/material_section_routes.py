"""Routes for material sections."""
from app.controllers.models.material_section_controller import MaterialSectionController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("material_sections", MaterialSectionController)