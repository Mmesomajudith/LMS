"""Service operations for CMB items."""
from app.services.resource_service import ResourceService


class CMBItemService(ResourceService):
    RESOURCE = "cmb_items"