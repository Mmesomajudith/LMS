"""Compatibility imports for identity models."""
from app.model.user import User
from app.model.role import Role
from app.model.user_role import UserRole
from app.model.lecturer_approval_event import LecturerApprovalEvent

__all__ = ["User", "Role", "UserRole", "LecturerApprovalEvent"]
