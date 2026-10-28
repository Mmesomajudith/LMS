"""AI Gateway request ORM model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class AIGatewayRequest(Base):
    __tablename__ = "ai_gateway_requests"
    request_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False, index=True)
    purpose = Column(String(100), nullable=False)
    provider = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    user = relationship("User", back_populates="ai_gateway_requests")
    course = relationship("Course", back_populates="ai_gateway_requests")
    request_sources = relationship("AIGatewayRequestSource", back_populates="request", cascade="all, delete-orphan")
    sections = relationship("MaterialSection", secondary="ai_gateway_request_sources", back_populates="ai_gateway_requests")
