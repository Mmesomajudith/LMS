"""Database models package for the LMS.

Every physical table has one canonical ORM class in a dedicated module.
"""

from app.model.user import User
from app.model.role import Role
from app.model.user_role import UserRole, user_role_association
from app.model.lecturer_approval_event import LecturerApprovalEvent
from app.model.course import Course
from app.model.enrolment import Enrolment
from app.model.concept import Concept
from app.model.concept_prerequisite import ConceptPrerequisite
from app.model.material import Material
from app.model.material_section import MaterialSection
from app.model.material_section_concept import MaterialSectionConcept
from app.model.assignment import Assignment
from app.model.assignment_question import AssignmentQuestion
from app.model.question_concept import QuestionConcept
from app.model.submission import Submission
from app.model.mark import Mark
from app.model.cmb_item import CMBItem
from app.model.cmb_item_concept import CMBItemConcept
from app.model.diagnostic_session import DiagnosticSession
from app.model.response import Response
from app.model.candidate_explanation import CandidateExplanation
from app.model.intervention import Intervention
from app.model.recommended_resource import RecommendedResource
from app.model.followup_result import FollowupResult
from app.model.access_log import AccessLog
from app.model.ai_gateway_request import AIGatewayRequest
from app.model.ai_gateway_request_source import AIGatewayRequestSource

__all__ = [
    "User", "Role", "UserRole", "LecturerApprovalEvent", "user_role_association",
    "Course", "Enrolment", "Concept", "ConceptPrerequisite", "Material",
    "MaterialSection", "MaterialSectionConcept", "Assignment", "AssignmentQuestion",
    "QuestionConcept", "Submission", "Mark", "CMBItem", "CMBItemConcept",
    "DiagnosticSession", "Response", "CandidateExplanation", "Intervention",
    "RecommendedResource", "FollowupResult", "AccessLog", "AIGatewayRequest",
    "AIGatewayRequestSource",
]
