"""HTTP controller for CMB item concepts."""
from app.controllers.resource_controller import ResourceController
from app.services.models.cmb_item_concept_service import CMBItemConceptService


class CMBItemConceptController(ResourceController):
    SERVICE_CLASS = CMBItemConceptService