"""HTTP controller for access logs."""
from app.controllers.resource_controller import ResourceController
from app.services.models.access_log_service import AccessLogService


class AccessLogController(ResourceController):
    SERVICE_CLASS = AccessLogService