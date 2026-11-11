"""Routes for CRUD, search, and pagination across registered resources."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import model_controller
from app.database import get_db
from app.routes.models.access_log_routes import router as access_log_router
from app.routes.models.ai_gateway_request_routes import router as ai_gateway_request_router
from app.routes.models.ai_gateway_request_source_routes import router as ai_gateway_request_source_router
from app.routes.models.assignment_routes import router as assignment_router
from app.routes.models.assignment_question_routes import router as assignment_question_router
from app.routes.models.candidate_explanation_routes import router as candidate_explanation_router
from app.routes.models.cmb_item_routes import router as cmb_item_router
from app.routes.models.cmb_item_concept_routes import router as cmb_item_concept_router
from app.routes.models.concept_routes import router as concept_router
from app.routes.models.concept_prerequisite_routes import router as concept_prerequisite_router
from app.routes.models.course_routes import router as course_router
from app.routes.models.department_routes import router as department_router
from app.routes.models.diagnostic_session_routes import router as diagnostic_session_router
from app.routes.models.enrolment_routes import router as enrolment_router
from app.routes.models.faculty_routes import router as faculty_router
from app.routes.models.followup_result_routes import router as followup_result_router
from app.routes.models.intervention_routes import router as intervention_router
from app.routes.models.lecturer_approval_event_routes import router as lecturer_approval_event_router
from app.routes.models.mark_routes import router as mark_router
from app.routes.models.material_routes import router as material_router
from app.routes.models.material_section_routes import router as material_section_router
from app.routes.models.material_section_concept_routes import router as material_section_concept_router
from app.routes.models.question_concept_routes import router as question_concept_router
from app.routes.models.recommended_resource_routes import router as recommended_resource_router
from app.routes.models.response_routes import router as response_router
from app.routes.models.role_routes import router as role_router
from app.routes.models.submission_routes import router as submission_router
from app.routes.models.user_routes import router as user_router
from app.routes.models.user_role_routes import router as user_role_router

router = APIRouter(prefix="/api", tags=["resources"])


@router.get("")
def get_resources(db: Session = Depends(get_db)) -> list[str]:
    return model_controller.list_resources(db)


for resource_router in (
    access_log_router,
    ai_gateway_request_router,
    ai_gateway_request_source_router,
    assignment_router,
    assignment_question_router,
    candidate_explanation_router,
    cmb_item_router,
    cmb_item_concept_router,
    concept_router,
    concept_prerequisite_router,
    course_router,
    department_router,
    diagnostic_session_router,
    enrolment_router,
    faculty_router,
    followup_result_router,
    intervention_router,
    lecturer_approval_event_router,
    mark_router,
    material_router,
    material_section_router,
    material_section_concept_router,
    question_concept_router,
    recommended_resource_router,
    response_router,
    role_router,
    submission_router,
    user_router,
    user_role_router,
):
    router.include_router(resource_router)