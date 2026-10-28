"""Compatibility imports for audit and AI Gateway models."""
from app.model.access_log import AccessLog
from app.model.ai_gateway_request import AIGatewayRequest
from app.model.ai_gateway_request_source import AIGatewayRequestSource

__all__ = ["AccessLog", "AIGatewayRequest", "AIGatewayRequestSource"]
