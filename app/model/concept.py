"""Course concept ORM model."""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
class Concept(Base):
    __tablename__ = "concepts"
    concept_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    __table_args__ = (UniqueConstraint("course_id", "name", name="uq_course_concept_name"),)
    course = relationship("Course", back_populates="concepts")
    prerequisites = relationship("Concept", secondary="concept_prerequisites", primaryjoin="Concept.concept_id==ConceptPrerequisite.concept_id", secondaryjoin="Concept.concept_id==ConceptPrerequisite.prerequisite_concept_id", backref="prerequisite_for")
    material_sections = relationship("MaterialSection", secondary="material_section_concepts", back_populates="concepts")
    assignment_questions = relationship("AssignmentQuestion", secondary="question_concepts", back_populates="concepts")
    cmb_items = relationship("CMBItem", secondary="cmb_item_concepts", back_populates="concepts")
    candidate_explanations = relationship("CandidateExplanation", back_populates="concept", cascade="all, delete-orphan")
