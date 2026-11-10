"""Routes for CRUD, search, and pagination across registered resources."""

from typing import Any

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from app.controllers import model_controller
from app.database import get_db

router = APIRouter(prefix="/api", tags=["resources"])


@router.get("")
def get_resources(db: Session = Depends(get_db)) -> list[str]:
    return model_controller.list_resources(db)


@router.get("/{resource}")
def get_records(
    resource: str,
    q: str | None = Query(default=None, description="Case-insensitive text search"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return model_controller.list_records(
        db, resource, query=q, page=page, page_size=page_size
    )


@router.post("/{resource}", status_code=201)
def insert_record(
    resource: str,
    data: dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return model_controller.insert_record(db, resource, data)


@router.patch("/{resource}/{record_id}")
def update_record(
    resource: str,
    record_id: str,
    data: dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return model_controller.update_record(db, resource, record_id, data)


@router.delete("/{resource}/{record_id}")
def delete_record(
    resource: str, record_id: str, db: Session = Depends(get_db)
) -> dict[str, str]:
    return model_controller.delete_record(db, resource, record_id)


@router.delete("/{resource}")
def delete_all_records(
    resource: str,
    confirm: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict[str, int]:
    return model_controller.delete_all_records(db, resource, confirm=confirm)