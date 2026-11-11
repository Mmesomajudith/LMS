"""Base service for a single model-backed resource."""

from typing import Any

from sqlalchemy.orm import Session

from app.services.model_service import ModelService


class ResourceService(ModelService):
    RESOURCE: str

    def __init__(self, db: Session):
        super().__init__(db)
        self.resource = self.RESOURCE

    def get_page(
        self, *, query: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        return super().list_records(
            self.resource, query=query, page=page, page_size=page_size
        )

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        return super().insert(self.resource, data)

    def update_record(
        self, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return super().update(self.resource, record_id, data)

    def delete_record(self, record_id: str) -> None:
        super().delete(self.resource, record_id)

    def delete_all_records(self) -> int:
        return super().delete_all(self.resource)