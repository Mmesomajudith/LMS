"""User-Role association re-export for backward compatibility."""

from app.model.identity import UserRole

user_role_association = UserRole.__table__

__all__ = ["UserRole", "user_role_association"]
