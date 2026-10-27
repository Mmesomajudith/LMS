"""Audit and AI Gateway models.

Defines polymorphic security/access audit logs, AI Gateway request tracking,
and the source passages passed to external AI providers for grounding.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class AccessLog(Base):
    """Audit log recording user actions, release events, and record views."""

    __tablename__ = "access_logs"

    log_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    target_type = Column(String(100), nullable=False, index=True)
    target_id = Column(String(100), nullable=False, index=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    user = relationship("User", back_populates="access_logs")

    def __repr__(self) -> str:
        return f"<AccessLog(log_id={self.log_id}, user={self.user_id}, action='{self.action}', target='{self.target_type}:{self.target_id}')>"


class AIGatewayRequest(Base):
    """Audit record of calls routed through the AI Gateway to external LLMs."""

    __tablename__ = "ai_gateway_requests"

    request_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    purpose = Column(String(100), nullable=False)
    provider = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    user = relationship("User", back_populates="ai_gateway_requests")
    course = relationship("Course", back_populates="ai_gateway_requests")
    request_sources = relationship(
        "AIGatewayRequestSource",
        back_populates="request",
        cascade="all, delete-orphan",
        overlaps="ai_gateway_requests,sections",
    )
    sections = relationship(
        "MaterialSection",
        secondary="ai_gateway_request_sources",
        back_populates="ai_gateway_requests",
        overlaps="request_sources,ai_gateway_request_sources",
    )

    def __repr__(self) -> str:
        return f"<AIGatewayRequest(request_id={self.request_id}, user={self.user_id}, purpose='{self.purpose}', status='{self.status}')>"


class AIGatewayRequestSource(Base):
    """Junction recording which lecturer-approved sections grounded an AI Gateway request."""

    __tablename__ = "ai_gateway_request_sources"

    request_id = Column(Integer, ForeignKey("ai_gateway_requests.request_id", ondelete="CASCADE"), primary_key=True)
    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)

    request = relationship(
        "AIGatewayRequest",
        back_populates="request_sources",
        overlaps="ai_gateway_requests,sections",
    )
    section = relationship(
        "MaterialSection",
        back_populates="ai_gateway_request_sources",
        overlaps="ai_gateway_requests,sections",
    )

    def __repr__(self) -> str:
        return f"<AIGatewayRequestSource(request_id={self.request_id}, section_id={self.section_id})>"
