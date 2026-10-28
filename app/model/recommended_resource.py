"""Recommended resource ORM model."""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class RecommendedResource(Base):
    __tablename__ = "recommended_resources"
    intervention_id = Column(Integer, ForeignKey("interventions.intervention_id", ondelete="CASCADE"), primary_key=True)
    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)
    reason = Column(Text, nullable=True)
    intervention = relationship("Intervention", back_populates="recommended_resources")
    section = relationship("MaterialSection", back_populates="recommended_resources")
