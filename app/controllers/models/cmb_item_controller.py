"""HTTP controller for CMB items."""
from app.controllers.resource_controller import ResourceController
from app.services.models.cmb_item_service import CMBItemService


class CMBItemController(ResourceController):
    SERVICE_CLASS = CMBItemService