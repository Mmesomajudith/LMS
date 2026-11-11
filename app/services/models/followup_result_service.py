"""Service operations for follow-up results."""
from app.services.resource_service import ResourceService


class FollowupResultService(ResourceService):
    RESOURCE = "followup_results"