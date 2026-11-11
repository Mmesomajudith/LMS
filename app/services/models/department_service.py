"""Service operations for departments."""
from app.services.resource_service import ResourceService


class DepartmentService(ResourceService):
    RESOURCE = "departments"