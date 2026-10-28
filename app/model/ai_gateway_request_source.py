"""AI Gateway source association ORM model."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class AIGatewayRequestSource(Base):
    __tablename__ = "ai_gateway_request_sources"
    request_id = Column(Integer, ForeignKey("ai_gateway_requests.request_id", ondelete="CASCADE"), primary_key=True)
    section_id = Column(Integer, ForeignKey("material_sections.section_id", ondelete="CASCADE"), primary_key=True)
    request = relationship("AIGatewayRequest", back_populates="request_sources")
    section = relationship("MaterialSection", back_populates="ai_gateway_request_sources")
