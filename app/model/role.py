"""Role ORM model."""
from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship, synonym
from app.database import Base
class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    __table_args__ = (CheckConstraint("name IN ('student', 'lecturer', 'administrator')", name="check_role_name"),)
    id = synonym("role_id")
    users = relationship("User", secondary="user_roles", back_populates="roles")
    user_roles = relationship("UserRole", foreign_keys="[UserRole.role_id]", back_populates="role", cascade="all, delete-orphan")
