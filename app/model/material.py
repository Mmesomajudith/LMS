"""Uploaded material ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class Material(Base):
    __tablename__ = "materials"
    material_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    file_path = Column(String(512), nullable=False)
    processing_status = Column(String(50), nullable=False, default="pending", server_default="pending")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    course = relationship("Course", back_populates="materials")
    uploader = relationship("User", back_populates="uploaded_materials")
    sections = relationship("MaterialSection", back_populates="material", cascade="all, delete-orphan", order_by="MaterialSection.section_order")
