"""Assignment ORM model."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Assignment(Base):
    __tablename__ = "assignments"
    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    lifecycle_status = Column(String(50), nullable=False, default="draft", server_default="draft")
    results_released_at = Column(DateTime(timezone=True), nullable=True)
    results_released_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    cmb_enabled = Column(Boolean, nullable=False, default=True, server_default="true")
    course = relationship("Course", back_populates="assignments")
    releaser = relationship("User", foreign_keys=[results_released_by])
    questions = relationship("AssignmentQuestion", back_populates="assignment", cascade="all, delete-orphan", order_by="AssignmentQuestion.position")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
