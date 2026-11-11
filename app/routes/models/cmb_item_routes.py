"""Routes for CMB items."""
from app.controllers.models.cmb_item_controller import CMBItemController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("cmb_items", CMBItemController)