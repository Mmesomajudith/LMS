"""Concept-to-Mastery Bridge (CMB) models.

Defines CMB items, item-concept links, diagnostic sessions, student responses,
candidate explanations (hypotheses), interventions, recommended resources,
and follow-up verification results.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class CMBItem(Base):
    """Reusable diagnostic, practice, or verification item approved by lecturers."""

    __tablename__ = "cmb_items"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = Column(String(50), nullable=False)  # 'diagnostic', 'practice', or 'verification'
    prompt = Column(Text, nullable=False)
    review_status = Column(String(50), nullable=False, default="draft", server_default="draft")
    approved_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('diagnostic', 'practice', 'verification')",
            name="check_cmb_item_type",
        ),
    )

    course = relationship("Course", back_populates="cmb_items")
    approver = relationship("User", foreign_keys=[approved_by])
    concepts = relationship(
        "Concept",
        secondary="cmb_item_concepts",
        back_populates="cmb_items",
    )
    responses = relationship("Response", back_populates="item", cascade="all, delete-orphan")
    followup_results = relationship("FollowupResult", back_populates="item", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CMBItem(item_id={self.item_id}, type='{self.item_type}', status='{self.review_status}')>"


class CMBItemConcept(Base):
    """Junction mapping CMB items to target pedagogical concepts."""

    __tablename__ = "cmb_item_concepts"

    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self) -> str:
        return f"<CMBItemConcept(item_id={self.item_id}, concept_id={self.concept_id})>"


class DiagnosticSession(Base):
    """A learning-gap diagnosis session initiated by a student following marked results."""

    __tablename__ = "diagnostic_sessions"

    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    submission = relationship("Submission", back_populates="diagnostic_sessions")
    responses = relationship("Response", back_populates="session", cascade="all, delete-orphan")
    candidate_explanations = relationship(
        "CandidateExplanation",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<DiagnosticSession(session_id={self.session_id}, submission_id={self.submission_id})>"


class Response(Base):
    """A student's answer and metacognitive confidence rating for a diagnostic item."""

    __tablename__ = "responses"

    response_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("diagnostic_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="RESTRICT"), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    confidence_choice = Column(String(50), nullable=True)  # e.g., 'high', 'medium', 'low', 'unsure'
    response_time = Column(Integer, nullable=True)  # in seconds

    session = relationship("DiagnosticSession", back_populates="responses")
    item = relationship("CMBItem", back_populates="responses")

    def __repr__(self) -> str:
        return f"<Response(response_id={self.response_id}, session_id={self.session_id}, item_id={self.item_id})>"


class CandidateExplanation(Base):
    """A probabilistic hypothesis regarding a misconception or learning gap."""

    __tablename__ = "candidate_explanations"

    explanation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("diagnostic_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)

    session = relationship("DiagnosticSession", back_populates="candidate_explanations")
    concept = relationship("Concept", back_populates="candidate_explanations")
    interventions = relationship("Intervention", back_populates="explanation", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<CandidateExplanation(explanation_id={self.explanation_id}, concept_id={self.concept_id}, label='{self.label}')>"


class Intervention(Base):
    """A targeted remediation plan triggered by a candidate explanation."""

    __tablename__ = "interventions"

    intervention_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    explanation_id = Column(Integer, ForeignKey("candidate_explanations.explanation_id", ondelete="CASCADE"), nullable=False, index=True)

    explanation = relationship("CandidateExplanation", back_populates="interventions")
    recommended_resources = relationship(
        "RecommendedResource",
        back_populates="intervention",
        cascade="all, delete-orphan",
    )
    followup_results = relationship(
        "FollowupResult",
        back_populates="intervention",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Intervention(intervention_id={self.intervention_id}, explanation_id={self.explanation_id})>"


class RecommendedResource(Base):
    """Link between an intervention and a specific lecturer-authored material section."""

    __tablename__ = "recommended_resources"

    intervention_id = Column(Integer, ForeignKey("interventions.intervention_id", ondelete="CASCADE"), primary_key=True)
    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)
    reason = Column(Text, nullable=True)

    intervention = relationship("Intervention", back_populates="recommended_resources")
    section = relationship("MaterialSection", back_populates="recommended_resources")

    def __repr__(self) -> str:
        return f"<RecommendedResource(intervention_id={self.intervention_id}, section_id={self.section_id})>"


class FollowupResult(Base):
    """The verification outcome measuring whether learning improved using a fresh item."""

    __tablename__ = "followup_results"

    followup_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    intervention_id = Column(Integer, ForeignKey("interventions.intervention_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="RESTRICT"), nullable=False, index=True)
    correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    intervention = relationship("Intervention", back_populates="followup_results")
    item = relationship("CMBItem", back_populates="followup_results")

    def __repr__(self) -> str:
        return f"<FollowupResult(followup_id={self.followup_id}, correct={self.correct})>"
