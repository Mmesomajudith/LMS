"""Base HTTP controller for a single model-backed resource."""

from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.controllers.model_controller import _handle_repository_error
from app.repositories.model_repository import RepositoryError
from app.services.resource_service import ResourceService


class ResourceController:
    SERVICE_CLASS: type[ResourceService]

    def __init__(self, db: Session):
        self.service = self.SERVICE_CLASS(db)

    def list_records(
        self, *, query: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        try:
            return jsonable_encoder(
                self.service.get_page(
                    query=query, page=page, page_size=page_size
                )
            )
        except RepositoryError as error:
            _handle_repository_error(error)

    def create_record(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            return jsonable_encoder(self.service.create(data))
        except RepositoryError as error:
            _handle_repository_error(error)

    def update_record(
        self, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            return jsonable_encoder(self.service.update_record(record_id, data))
        except RepositoryError as error:
            _handle_repository_error(error)

    def delete_record(self, record_id: str) -> dict[str, str]:
        try:
            self.service.delete_record(record_id)
            return {"detail": "Record deleted"}
        except RepositoryError as error:
            _handle_repository_error(error)

    def delete_all_records(self, *, confirm: bool) -> dict[str, int]:
        if not confirm:
            raise HTTPException(
                status_code=400,
                detail="Set confirm=true to delete every record in this resource",
            )
        try:
            return {"deleted": self.service.delete_all_records()}
        except RepositoryError as error:
            _handle_repository_error(error)