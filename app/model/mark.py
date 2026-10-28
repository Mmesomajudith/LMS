"""Question mark ORM model."""
from sqlalchemy import Column, Integer, Numeric, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class Mark(Base):
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
