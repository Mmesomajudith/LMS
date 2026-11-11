"""Factory for standard CRUD routes bound to one resource controller."""

from typing import Any

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from app.controllers.resource_controller import ResourceController
from app.database import get_db


def create_resource_router(
    resource: str, controller_class: type[ResourceController]
) -> APIRouter:
    router = APIRouter(prefix=f"/{resource}", tags=[resource])

    @router.get("")
    def get_records(
        q: str | None = Query(default=None, description="Case-insensitive text search"),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=25, ge=1, le=100),
        db: Session = Depends(get_db),
    ) -> dict[str, Any]:
        return controller_class(db).list_records(
            query=q, page=page, page_size=page_size
        )

    @router.post("", status_code=201)
    def insert_record(
        data: dict[str, Any] = Body(...), db: Session = Depends(get_db)
    ) -> dict[str, Any]:
        return controller_class(db).create_record(data)

    @router.patch("/{record_id}")
    def update_record(
        record_id: str,
        data: dict[str, Any] = Body(...),
        db: Session = Depends(get_db),
    ) -> dict[str, Any]:
        return controller_class(db).update_record(record_id, data)

    @router.delete("/{record_id}")
    def delete_record(
        record_id: str, db: Session = Depends(get_db)
    ) -> dict[str, str]:
        return controller_class(db).delete_record(record_id)

    @router.delete("")
    def delete_all_records(
        confirm: bool = Query(default=False), db: Session = Depends(get_db)
    ) -> dict[str, int]:
        return controller_class(db).delete_all_records(confirm=confirm)

    return router