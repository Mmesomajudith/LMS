"""Compatibility imports for assessment models."""
from app.model.assignment import Assignment
from app.model.assignment_question import AssignmentQuestion
from app.model.question_concept import QuestionConcept
from app.model.submission import Submission
from app.model.mark import Mark

__all__ = ["Assignment", "AssignmentQuestion", "QuestionConcept", "Submission", "Mark"]
