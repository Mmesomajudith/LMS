"""Submission ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base
class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    work_reference = Column(String(512), nullable=False)
    marking_status = Column(String(50), nullable=False, default="submitted", server_default="submitted")
    __table_args__ = (UniqueConstraint("assignment_id", "user_id", name="uq_assignment_submission_user"),)
    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    marks = relationship("Mark", back_populates="submission", cascade="all, delete-orphan")
    diagnostic_sessions = relationship("DiagnosticSession", back_populates="submission", cascade="all, delete-orphan")
