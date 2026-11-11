"""Routes for access logs."""
from app.controllers.models.access_log_controller import AccessLogController
from app.routes.resource_routes import create_resource_router

router = create_resource_router("access_logs", AccessLogController)