"""Material-section concept association ORM model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class MaterialSectionConcept(Base):
    __tablename__ = "material_section_concepts"
    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
