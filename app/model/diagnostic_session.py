"""Diagnostic session ORM model."""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class DiagnosticSession(Base):
    __tablename__ = "diagnostic_sessions"
    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    submission = relationship("Submission", back_populates="diagnostic_sessions")
    responses = relationship("Response", back_populates="session", cascade="all, delete-orphan")
    candidate_explanations = relationship("CandidateExplanation", back_populates="session", cascade="all, delete-orphan")
