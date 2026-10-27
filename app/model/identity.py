"""Identity and Access Control models.

Defines users, roles, user role assignments, and administrator approval events
for lecturers, following the approved LMS schema and 3NF normalization.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship, synonym
from app.database import Base


class User(Base):
    """Represents a system user (student, lecturer, or administrator)."""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    account_status = Column(String(50), nullable=False, default="active", server_default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Aliases for backward compatibility
    id = synonym("user_id")
    password = synonym("password_hash")

    # Access control relationships
    roles = relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="User.user_id == UserRole.user_id",
        secondaryjoin="Role.role_id == UserRole.role_id",
        back_populates="users",
    )
    user_roles = relationship(
        "UserRole",
        foreign_keys="[UserRole.user_id]",
        back_populates="user",
        cascade="all, delete-orphan",
        overlaps="roles",
    )
    lecturer_approvals_received = relationship(
        "LecturerApprovalEvent",
        foreign_keys="[LecturerApprovalEvent.lecturer_user_id]",
        back_populates="lecturer",
        cascade="all, delete-orphan",
    )
    lecturer_approvals_given = relationship(
        "LecturerApprovalEvent",
        foreign_keys="[LecturerApprovalEvent.administrator_user_id]",
        back_populates="administrator",
    )

    # Course, Assessment, and Learning relationships
    owned_courses = relationship("Course", back_populates="owner", cascade="all, delete-orphan")
    enrolments = relationship("Enrolment", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    uploaded_materials = relationship("Material", back_populates="uploader")

    # Audit & Gateway relationships
    access_logs = relationship("AccessLog", back_populates="user")
    ai_gateway_requests = relationship("AIGatewayRequest", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id}, email='{self.email}', status='{self.account_status}')>"


class Role(Base):
    """Represents a system role (e.g. 'student', 'lecturer', 'administrator')."""

    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

    # Alias for backward compatibility
    id = synonym("role_id")

    users = relationship(
        "User",
        secondary="user_roles",
        primaryjoin="Role.role_id == UserRole.role_id",
        secondaryjoin="User.user_id == UserRole.user_id",
        back_populates="roles",
        overlaps="user_roles",
    )
    user_roles = relationship(
        "UserRole",
        foreign_keys="[UserRole.role_id]",
        back_populates="role",
        cascade="all, delete-orphan",
        overlaps="roles,users",
    )

    def __repr__(self) -> str:
        return f"<Role(role_id={self.role_id}, name='{self.name}')>"


class UserRole(Base):
    """Association model linking users and roles with assignment metadata."""

    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles", overlaps="roles,users")
    role = relationship("Role", foreign_keys=[role_id], back_populates="user_roles", overlaps="roles,users")
    assigner = relationship("User", foreign_keys=[assigned_by])

    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id}, assigned_by={self.assigned_by})>"


class LecturerApprovalEvent(Base):
    """Audit trail of administrator decisions on lecturer registration requests."""

    __tablename__ = "lecturer_approval_events"

    approval_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lecturer_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    administrator_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    decision = Column(String(50), nullable=False)
    decided_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("decision IN ('approved', 'rejected')", name="check_approval_decision"),
    )

    lecturer = relationship("User", foreign_keys=[lecturer_user_id], back_populates="lecturer_approvals_received")
    administrator = relationship("User", foreign_keys=[administrator_user_id], back_populates="lecturer_approvals_given")

    def __repr__(self) -> str:
        return f"<LecturerApprovalEvent(approval_id={self.approval_id}, lecturer={self.lecturer_user_id}, decision='{self.decision}')>"
