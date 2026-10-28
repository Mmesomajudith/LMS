"""Course enrolment ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class Enrolment(Base):
    __tablename__ = "enrolments"
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    status = Column(String(50), nullable=False, default="enrolled", server_default="enrolled")
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    course = relationship("Course", back_populates="enrolments")
    user = relationship("User", back_populates="enrolments")
