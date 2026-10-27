"""Assessment models.

Defines assignments, assignment questions, question-concept associations,
student submissions, and question-level marks and feedback.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Numeric,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Assignment(Base):
    """Represents a graded assignment within a course with CMB enablement and release gates."""

    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    lifecycle_status = Column(String(50), nullable=False, default="draft", server_default="draft")
    results_released_at = Column(DateTime(timezone=True), nullable=True)
    results_released_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    cmb_enabled = Column(Boolean, nullable=False, default=True, server_default="true")

    # Relationships
    course = relationship("Course", back_populates="assignments")
    releaser = relationship("User", foreign_keys=[results_released_by])
    questions = relationship(
        "AssignmentQuestion",
        back_populates="assignment",
        cascade="all, delete-orphan",
        order_by="AssignmentQuestion.position",
    )
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Assignment(assignment_id={self.assignment_id}, title='{self.title}', status='{self.lifecycle_status}')>"


class AssignmentQuestion(Base):
    """An individual question item belonging to an assignment."""

    __tablename__ = "assignment_questions"

    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    max_score = Column(Numeric(5, 2), nullable=False)
    position = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("assignment_id", "position", name="uq_assignment_question_position"),
    )

    assignment = relationship("Assignment", back_populates="questions")
    concepts = relationship(
        "Concept",
        secondary="question_concepts",
        back_populates="assignment_questions",
    )
    marks = relationship("Mark", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AssignmentQuestion(question_id={self.question_id}, assignment_id={self.assignment_id}, pos={self.position})>"


class QuestionConcept(Base):
    """Junction mapping assignment questions to target pedagogical concepts."""

    __tablename__ = "question_concepts"

    question_id = Column(Integer, ForeignKey("assignment_questions.question_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self) -> str:
        return f"<QuestionConcept(question_id={self.question_id}, concept_id={self.concept_id})>"


class Submission(Base):
    """A student's submitted coursework attempt for an assignment."""

    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    work_reference = Column(String(512), nullable=False)
    marking_status = Column(String(50), nullable=False, default="submitted", server_default="submitted")

    __table_args__ = (
        UniqueConstraint("assignment_id", "user_id", name="uq_assignment_submission_user"),
    )

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    marks = relationship("Mark", back_populates="submission", cascade="all, delete-orphan")
    diagnostic_sessions = relationship("DiagnosticSession", back_populates="submission", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Submission(submission_id={self.submission_id}, assignment_id={self.assignment_id}, user_id={self.user_id})>"


class Mark(Base):
    """Question-level evaluation awarded by a lecturer with scores and comments."""

    __tablename__ = "marks"

    submission_id = Column(Integer, ForeignKey("submissions.submission_id", ondelete="CASCADE"), primary_key=True)
    question_id = Column(Integer, ForeignKey("assignment_questions.question_id", ondelete="CASCADE"), primary_key=True)
    score = Column(Numeric(5, 2), nullable=False)
    lecturer_comment = Column(Text, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    graded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    submission = relationship("Submission", back_populates="marks")
    question = relationship("AssignmentQuestion", back_populates="marks")
    grader = relationship("User", foreign_keys=[graded_by])

    def __repr__(self) -> str:
        return f"<Mark(submission_id={self.submission_id}, question_id={self.question_id}, score={self.score})>"
