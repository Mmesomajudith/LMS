"""Service operations for access logs."""
from app.services.resource_service import ResourceService


class AccessLogService(ResourceService):
    RESOURCE = "access_logs"