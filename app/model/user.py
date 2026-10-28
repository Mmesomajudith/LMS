"""User ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, func
from sqlalchemy.orm import relationship, synonym
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    account_status = Column(String(50), nullable=False, default="active", server_default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (CheckConstraint("account_status IN ('active', 'inactive', 'disabled')", name="check_user_account_status"),)
    id = synonym("user_id")
    password = synonym("password_hash")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    user_roles = relationship("UserRole", foreign_keys="[UserRole.user_id]", back_populates="user", cascade="all, delete-orphan", overlaps="roles")
    lecturer_approvals_received = relationship("LecturerApprovalEvent", foreign_keys="[LecturerApprovalEvent.lecturer_user_id]", back_populates="lecturer", cascade="all, delete-orphan")
    lecturer_approvals_given = relationship("LecturerApprovalEvent", foreign_keys="[LecturerApprovalEvent.administrator_user_id]", back_populates="administrator")
    owned_courses = relationship("Course", back_populates="owner", cascade="all, delete-orphan")
    enrolments = relationship("Enrolment", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    uploaded_materials = relationship("Material", back_populates="uploader")
    access_logs = relationship("AccessLog", back_populates="user")
    ai_gateway_requests = relationship("AIGatewayRequest", back_populates="user")
