"""Service operations for submissions."""
from app.services.resource_service import ResourceService


class SubmissionService(ResourceService):
    RESOURCE = "submissions"