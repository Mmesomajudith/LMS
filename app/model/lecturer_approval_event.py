"""Lecturer approval event ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base
class LecturerApprovalEvent(Base):
    __tablename__ = "lecturer_approval_events"
    approval_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lecturer_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    administrator_user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    decision = Column(String(50), nullable=False)
    decided_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (CheckConstraint("decision IN ('approved', 'rejected')", name="check_approval_decision"),)
    lecturer = relationship("User", foreign_keys=[lecturer_user_id], back_populates="lecturer_approvals_received")
    administrator = relationship("User", foreign_keys=[administrator_user_id], back_populates="lecturer_approvals_given")
