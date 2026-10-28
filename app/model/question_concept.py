"""Question-concept association ORM model."""
from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
class QuestionConcept(Base):
    __tablename__ = "question_concepts"
    question_id = Column(Integer, ForeignKey("assignment_questions.question_id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(Integer, ForeignKey("concepts.concept_id", ondelete="CASCADE"), primary_key=True)
