"""Faculty academic entity ORM model."""
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    faculty_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", name="uq_faculty_name"),
        UniqueConstraint("code", name="uq_faculty_code"),
    )

    departments = relationship("Department", back_populates="faculty", cascade="all, delete-orphan")
