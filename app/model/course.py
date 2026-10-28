"""Course ORM model."""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Course(Base):
    """Represents an academic course owned by a lecturer."""

    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    ai_enabled = Column(Boolean, nullable=False, default=True, server_default="true")

    owner = relationship("User", back_populates="owned_courses")
    enrolments = relationship("Enrolment", back_populates="course", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="course", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    cmb_items = relationship("CMBItem", back_populates="course", cascade="all, delete-orphan")
    ai_gateway_requests = relationship("AIGatewayRequest", back_populates="course", cascade="all, delete-orphan")
