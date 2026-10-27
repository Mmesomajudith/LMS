"""Database models package for LMS.

Exports all ORM models for identity, courses, materials, assessments,
Concept-to-Mastery Bridge (CMB), and audit/gateway tracking.
"""

from app.model.identity import (
    User,
    Role,
    UserRole,
    LecturerApprovalEvent,
)
from app.model.course import (
    Course,
    Enrolment,
    Concept,
    ConceptPrerequisite,
    Material,
    MaterialSection,
    MaterialSectionConcept,
)
from app.model.assessment import (
    Assignment,
    AssignmentQuestion,
    QuestionConcept,
    Submission,
    Mark,
)
from app.model.cmb import (
    CMBItem,
    CMBItemConcept,
    DiagnosticSession,
    Response,
    CandidateExplanation,
    Intervention,
    RecommendedResource,
    FollowupResult,
)
from app.model.audit import (
    AccessLog,
    AIGatewayRequest,
    AIGatewayRequestSource,
)

# Alias for backward compatibility with existing seeds and migrations
user_role_association = UserRole.__table__

__all__ = [
    # Identity and Access
    "User",
    "Role",
    "UserRole",
    "LecturerApprovalEvent",
    "user_role_association",
    # Courses and Materials
    "Course",
    "Enrolment",
    "Concept",
    "ConceptPrerequisite",
    "Material",
    "MaterialSection",
    "MaterialSectionConcept",
    # Assessment
    "Assignment",
    "AssignmentQuestion",
    "QuestionConcept",
    "Submission",
    "Mark",
    # Concept-to-Mastery Bridge (CMB)
    "CMBItem",
    "CMBItemConcept",
    "DiagnosticSession",
    "Response",
    "CandidateExplanation",
    "Intervention",
    "RecommendedResource",
    "FollowupResult",
    # Audit and Gateway
    "AccessLog",
    "AIGatewayRequest",
    "AIGatewayRequestSource",
]
