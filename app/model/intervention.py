"""Intervention ORM model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Intervention(Base):
    __tablename__ = "interventions"
    intervention_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    explanation_id = Column(Integer, ForeignKey("candidate_explanations.explanation_id", ondelete="CASCADE"), nullable=False, index=True)
    explanation = relationship("CandidateExplanation", back_populates="interventions")
    recommended_resources = relationship("RecommendedResource", back_populates="intervention", cascade="all, delete-orphan")
    followup_results = relationship("FollowupResult", back_populates="intervention", cascade="all, delete-orphan")
