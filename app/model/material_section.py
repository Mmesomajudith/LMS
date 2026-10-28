"""Material section ORM model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
class MaterialSection(Base):
    __tablename__ = "material_sections"
    section_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey("materials.material_id", ondelete="CASCADE"), nullable=False, index=True)
    section_order = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    source_location_type = Column(String(50), nullable=False)
    source_location_value = Column(String(100), nullable=False)
    __table_args__ = (UniqueConstraint("material_id", "section_order", name="uq_material_section_order"),)
    material = relationship("Material", back_populates="sections")
    concepts = relationship("Concept", secondary="material_section_concepts", back_populates="material_sections")
    recommended_resources = relationship("RecommendedResource", back_populates="section", cascade="all, delete-orphan")
    ai_gateway_requests = relationship("AIGatewayRequest", secondary="ai_gateway_request_sources", back_populates="sections")
    ai_gateway_request_sources = relationship("AIGatewayRequestSource", back_populates="section", cascade="all, delete-orphan")
