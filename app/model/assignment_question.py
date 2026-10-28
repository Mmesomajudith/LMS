"""Assignment question ORM model."""
from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
class AssignmentQuestion(Base):
    __tablename__ = "assignment_questions"
    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    max_score = Column(Numeric(5, 2), nullable=False)
    position = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint("assignment_id", "position", name="uq_assignment_question_position"),)
    assignment = relationship("Assignment", back_populates="questions")
    concepts = relationship("Concept", secondary="question_concepts", back_populates="assignment_questions")
    marks = relationship("Mark", back_populates="question", cascade="all, delete-orphan")
