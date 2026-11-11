"""Routes for follow-up results."""
from app.controllers.models.followup_result_controller import FollowupResultController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("followup_results", FollowupResultController)