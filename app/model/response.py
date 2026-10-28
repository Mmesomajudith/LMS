"""Student response ORM model."""
from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Response(Base):
    __tablename__ = "responses"
    response_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("diagnostic_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="RESTRICT"), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    confidence_choice = Column(String(50), nullable=True)
    response_time = Column(Integer, nullable=True)
    session = relationship("DiagnosticSession", back_populates="responses")
    item = relationship("CMBItem", back_populates="responses")
