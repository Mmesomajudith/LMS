"""HTTP controller for follow-up results."""
from app.controllers.resource_controller import ResourceController
from app.services.models.followup_result_service import FollowupResultService


class FollowupResultController(ResourceController):
    SERVICE_CLASS = FollowupResultService