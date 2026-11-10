"""Business operations for model-backed resources."""

from typing import Any

from sqlalchemy.orm import Session

from app.repositories.model_repository import ModelRepository


class ModelService:
    def __init__(self, db: Session):
        self.repository = ModelRepository(db)

    def resources(self) -> list[str]:
        return self.repository.resources()

    def list_records(
        self, resource: str, *, query: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        records, total = self.repository.list_records(
            resource,
            query=query,
            offset=(page - 1) * page_size,
            limit=page_size,
        )
        return {
            "items": records,
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size,
        }

    def insert(self, resource: str, data: dict[str, Any]) -> dict[str, Any]:
        return self.repository.insert(resource, data)

    def update(
        self, resource: str, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return self.repository.update(resource, record_id, data)

    def delete(self, resource: str, record_id: str) -> None:
        self.repository.delete(resource, record_id)

    def delete_all(self, resource: str) -> int:
        return self.repository.delete_all(resource)

    def seed_demo_data(self) -> None:
        administrator = self.insert("roles", {"name": "administrator"})
        self.insert("roles", {"name": "lecturer"})
        self.insert("roles", {"name": "student"})
        user = self.insert(
            "users",
            {
                "username": "johndoe",
                "email": "john@example.com",
                "password_hash": "hashed_password",
            },
        )
        self.insert(
            "user_roles",
            {"user_id": user["user_id"], "role_id": administrator["role_id"]},
        )