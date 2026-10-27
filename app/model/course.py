"""Course and Material models.

Defines courses, enrolments, pedagogical concepts, prerequisite graphs,
course materials, extracted sections, and section-concept associations.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Course(Base):
    """Represents an academic course owned by a lecturer."""

    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    ai_enabled = Column(Boolean, nullable=False, default=True, server_default="true")

    # Relationships
    owner = relationship("User", back_populates="owned_courses")
    enrolments = relationship("Enrolment", back_populates="course", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="course", cascade="all, delete-orphan")
    materials = relationship("Material", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    cmb_items = relationship("CMBItem", back_populates="course", cascade="all, delete-orphan")
    ai_gateway_requests = relationship("AIGatewayRequest", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Course(course_id={self.course_id}, title='{self.title}', owner={self.owner_user_id})>"


class Enrolment(Base):
    """Junction table connecting students to courses with enrolment status and date."""

    __tablename__ = "enrolments"

    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    status = Column(String(50), nullable=False, default="enrolled", server_default="enrolled")
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    course = relationship("Course", back_populates="enrolments")
    user = relationship("User", back_populates="enrolments")

    def __repr__(self) -> str:
        return f"<Enrolment(course_id={self.course_id}, user_id={self.user_id}, status='{self.status}')>"


class Concept(Base):
    """Represents a discrete topic or learning objective within a course."""

    __tablename__ = "concepts"

    concept_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint("course_id", "name", name="uq_course_concept_name"),
    )

    course = relationship("Course", back_populates="concepts")

    # Directed prerequisite graph relationships
    prerequisites = relationship(
        "Concept",
        secondary="concept_prerequisites",
        primaryjoin="Concept.concept_id==ConceptPrerequisite.concept_id",
        secondaryjoin="Concept.concept_id==ConceptPrerequisite.prerequisite_concept_id",
        backref="prerequisite_for",
    )

    # Content mappings
    material_sections = relationship(
        "MaterialSection",
        secondary="material_section_concepts",
        back_populates="concepts",
    )
    assignment_questions = relationship(
        "AssignmentQuestion",
        secondary="question_concepts",
        back_populates="concepts",
    )
    cmb_items = relationship(
        "CMBItem",
        secondary="cmb_item_concepts",
        back_populates="concepts",
    )
    candidate_explanations = relationship(
        "CandidateExplanation",
        back_populates="concept",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Concept(concept_id={self.concept_id}, course_id={self.course_id}, name='{self.name}')>"


class ConceptPrerequisite(Base):
    """Directed dependency between two concepts in the prerequisite graph."""

    __tablename__ = "concept_prerequisites"

    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
    prerequisite_concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        CheckConstraint("concept_id != prerequisite_concept_id", name="check_concept_not_self_prerequisite"),
    )

    def __repr__(self) -> str:
        return f"<ConceptPrerequisite(concept_id={self.concept_id}, prerequisite_concept_id={self.prerequisite_concept_id})>"


class Material(Base):
    """Represents an uploaded lecture document (PDF, slides, notes)."""

    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    processing_status = Column(String(50), nullable=False, default="pending", server_default="pending")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    course = relationship("Course", back_populates="materials")
    uploader = relationship("User", back_populates="uploaded_materials")
    sections = relationship(
        "MaterialSection",
        back_populates="material",
        cascade="all, delete-orphan",
        order_by="MaterialSection.section_order",
    )

    def __repr__(self) -> str:
        return f"<Material(material_id={self.material_id}, course_id={self.course_id}, status='{self.processing_status}')>"


class MaterialSection(Base):
    """A citable passage or slide chunk extracted from an uploaded document."""

    __tablename__ = "material_sections"

    section_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey("materials.material_id", ondelete="CASCADE"), nullable=False, index=True)
    section_order = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    source_location_type = Column(String(50), nullable=False)  # e.g., 'page', 'slide', 'section'
    source_location_value = Column(String(100), nullable=False)  # e.g., '14', 'Slide 7'

    __table_args__ = (
        UniqueConstraint("material_id", "section_order", name="uq_material_section_order"),
    )

    material = relationship("Material", back_populates="sections")
    concepts = relationship(
        "Concept",
        secondary="material_section_concepts",
        back_populates="material_sections",
    )
    recommended_resources = relationship("RecommendedResource", back_populates="section", cascade="all, delete-orphan")
    ai_gateway_requests = relationship(
        "AIGatewayRequest",
        secondary="ai_gateway_request_sources",
        back_populates="sections",
        overlaps="ai_gateway_request_sources,request_sources",
    )
    ai_gateway_request_sources = relationship(
        "AIGatewayRequestSource",
        back_populates="section",
        cascade="all, delete-orphan",
        overlaps="ai_gateway_requests,sections",
    )

    def __repr__(self) -> str:
        return f"<MaterialSection(section_id={self.section_id}, material_id={self.material_id}, order={self.section_order})>"


class MaterialSectionConcept(Base):
    """Junction mapping extracted material sections to pedagogical concepts."""

    __tablename__ = "material_section_concepts"

    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self) -> str:
        return f"<MaterialSectionConcept(section_id={self.section_id}, concept_id={self.concept_id})>"
