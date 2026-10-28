"""Candidate explanation ORM model."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class CandidateExplanation(Base):
    __tablename__ = "candidate_explanations"
    explanation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("diagnostic_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    session = relationship("DiagnosticSession", back_populates="candidate_explanations")
    concept = relationship("Concept", back_populates="candidate_explanations")
    interventions = relationship("Intervention", back_populates="explanation", cascade="all, delete-orphan")
