"""Follow-up verification result ORM model."""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
class FollowupResult(Base):
    __tablename__ = "followup_results"
    followup_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    intervention_id = Column(Integer, ForeignKey("interventions.intervention_id", ondelete="CASCADE"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="RESTRICT"), nullable=False, index=True)
    correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    intervention = relationship("Intervention", back_populates="followup_results")
    item = relationship("CMBItem", back_populates="followup_results")
