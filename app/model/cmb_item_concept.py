"""CMB item-concept association ORM model."""
from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
class CMBItemConcept(Base):
    __tablename__ = "cmb_item_concepts"
    item_id = Column(Integer, ForeignKey("cmb_items.item_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
