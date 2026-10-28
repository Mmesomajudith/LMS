"""Concept prerequisite association ORM model."""
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from app.database import Base
class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
    prerequisite_concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
    __table_args__ = (CheckConstraint("concept_id != prerequisite_concept_id", name="check_concept_not_self_prerequisite"),)
