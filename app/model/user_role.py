"""User-role association ORM model."""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles", overlaps="roles")
    role = relationship("Role", foreign_keys=[role_id], back_populates="user_roles")
    assigner = relationship("User", foreign_keys=[assigned_by])


user_role_association = UserRole.__table__

__all__ = ["UserRole", "user_role_association"]
