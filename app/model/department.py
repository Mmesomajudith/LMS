"""Department academic entity ORM model."""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    faculty_id = Column(Integer, ForeignKey("faculties.faculty_id", name="fk_departments_faculty_id_faculties", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("faculty_id", "name", name="uq_faculty_department_name"),
        UniqueConstraint("faculty_id", "code", name="uq_faculty_department_code"),
    )

    faculty = relationship("Faculty", back_populates="departments")
    users = relationship("User", back_populates="department")
    courses = relationship("Course", back_populates="department")
