"""CMB item ORM model."""
from sqlalchemy import Column, Integer, Text, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
class CMBItem(Base):
    __tablename__ = "cmb_items"
    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    item_type = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    review_status = Column(String(50), nullable=False, default="draft", server_default="draft")
    approved_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    __table_args__ = (CheckConstraint("item_type IN ('diagnostic', 'practice', 'verification')", name="check_cmb_item_type"),)
    course = relationship("Course", back_populates="cmb_items")
    approver = relationship("User", foreign_keys=[approved_by])
    concepts = relationship("Concept", secondary="cmb_item_concepts", back_populates="cmb_items")
    responses = relationship("Response", back_populates="item", cascade="all, delete-orphan")
    followup_results = relationship("FollowupResult", back_populates="item", cascade="all, delete-orphan")
