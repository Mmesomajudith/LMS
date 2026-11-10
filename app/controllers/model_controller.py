"""HTTP-facing controller for model-backed resources."""

from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.repositories.model_repository import (
    InvalidRecordError,
    InvalidRecordKeyError,
    RecordConflictError,
    RecordNotFoundError,
    ResourceNotFoundError,
)
from app.services.model_service import ModelService


def _handle_repository_error(error: Exception) -> None:
    if isinstance(error, ResourceNotFoundError):
        raise HTTPException(status_code=404, detail="Resource not found") from error
    if isinstance(error, RecordNotFoundError):
        raise HTTPException(status_code=404, detail="Record not found") from error
    if isinstance(error, InvalidRecordKeyError):
        raise HTTPException(status_code=422, detail=str(error)) from error
    if isinstance(error, InvalidRecordError):
        raise HTTPException(status_code=422, detail=str(error)) from error
    if isinstance(error, RecordConflictError):
        raise HTTPException(status_code=409, detail=str(error)) from error
    raise error


def list_resources(db: Session) -> list[str]:
    return ModelService(db).resources()


def list_records(
    db: Session, resource: str, *, query: str | None, page: int, page_size: int
) -> dict[str, Any]:
    try:
        result = ModelService(db).list_records(
            resource, query=query, page=page, page_size=page_size
        )
        return jsonable_encoder(result)
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)


def insert_record(db: Session, resource: str, data: dict[str, Any]) -> dict[str, Any]:
    try:
        return jsonable_encoder(ModelService(db).insert(resource, data))
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)


def update_record(
    db: Session, resource: str, record_id: str, data: dict[str, Any]
) -> dict[str, Any]:
    try:
        return jsonable_encoder(ModelService(db).update(resource, record_id, data))
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)


def delete_record(db: Session, resource: str, record_id: str) -> dict[str, str]:
    try:
        ModelService(db).delete(resource, record_id)
        return {"detail": "Record deleted"}
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)


def delete_all_records(db: Session, resource: str, *, confirm: bool) -> dict[str, int]:
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Set confirm=true to delete every record in this resource",
        )
    try:
        return {"deleted": ModelService(db).delete_all(resource)}
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)


def seed_demo_data(db: Session) -> dict[str, str]:
    try:
        ModelService(db).seed_demo_data()
        return {"message": "Data seeded successfully!"}
    except (ResourceNotFoundError, RecordNotFoundError, InvalidRecordKeyError,
            InvalidRecordError, RecordConflictError) as error:
        _handle_repository_error(error)