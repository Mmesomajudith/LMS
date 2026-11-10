"""Persistence operations for resources backed by registered ORM models."""

from typing import Any

from sqlalchemy import and_, delete, func, insert, or_, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import String

import app.model  # noqa: F401 - importing registers every model with Base.
from app.database import Base


class RepositoryError(Exception):
    """Base exception for repository operations."""


class ResourceNotFoundError(RepositoryError):
    pass


class RecordNotFoundError(RepositoryError):
    pass


class InvalidRecordError(RepositoryError):
    pass


class InvalidRecordKeyError(RepositoryError):
    pass


class RecordConflictError(RepositoryError):
    pass


class ModelRepository:
    """Encapsulates all table access for the service layer."""

    def __init__(self, db: Session):
        self.db = db
        self._tables = Base.metadata.tables

    def resources(self) -> list[str]:
        return sorted(self._tables)

    def _table_for(self, resource: str) -> Any:
        try:
            return self._tables[resource]
        except KeyError as error:
            raise ResourceNotFoundError(resource) from error

    @staticmethod
    def _record_for(table: Any, record: Any) -> dict[str, Any]:
        result = dict(record)
        result.pop("password_hash", None)
        return result

    @staticmethod
    def _validate_fields(table: Any, data: dict[str, Any], *, updating: bool) -> None:
        if updating and not data:
            raise InvalidRecordError("At least one field is required for an update")
        column_names = set(table.columns.keys())
        primary_keys = set(table.primary_key.columns.keys())
        allowed = column_names - (primary_keys if updating else set())
        invalid = set(data) - allowed
        if invalid:
            raise InvalidRecordError(
                f"Unsupported field(s): {', '.join(sorted(invalid))}"
            )

    @staticmethod
    def _parse_key(table: Any, record_id: str) -> dict[str, Any]:
        primary_keys = list(table.primary_key.columns)
        key_parts = record_id.split(",")
        if len(key_parts) != len(primary_keys):
            raise InvalidRecordKeyError(
                "Record key does not match the resource primary key"
            )

        values: dict[str, Any] = {}
        try:
            for column, raw_value in zip(primary_keys, key_parts):
                values[column.key] = column.type.python_type(raw_value)
        except (TypeError, ValueError, NotImplementedError) as error:
            raise InvalidRecordKeyError("Record key has an invalid value") from error
        return values

    @staticmethod
    def _key_conditions(table: Any, values: dict[str, Any]) -> list[Any]:
        return [table.c[name] == value for name, value in values.items()]

    def _get_record(self, table: Any, key_values: dict[str, Any]) -> Any:
        statement = select(table).where(
            and_(*self._key_conditions(table, key_values))
        )
        return self.db.execute(statement).mappings().one_or_none()

    def list_records(
        self, resource: str, *, query: str | None, offset: int, limit: int
    ) -> tuple[list[dict[str, Any]], int]:
        table = self._table_for(resource)
        filters = []
        if query:
            search_columns = [
                column.ilike(f"%{query}%")
                for column in table.columns
                if isinstance(column.type, String)
            ]
            if search_columns:
                filters.append(or_(*search_columns))

        count_statement = select(func.count()).select_from(table).where(*filters)
        total = self.db.execute(count_statement).scalar_one()
        statement = (
            select(table)
            .where(*filters)
            .order_by(*table.primary_key.columns)
            .offset(offset)
            .limit(limit)
        )
        records = self.db.execute(statement).mappings().all()
        return [self._record_for(table, record) for record in records], total

    def insert(self, resource: str, data: dict[str, Any]) -> dict[str, Any]:
        table = self._table_for(resource)
        self._validate_fields(table, data, updating=False)
        try:
            result = self.db.execute(insert(table).values(**data))
            self.db.commit()
            key_values = {
                column.key: data.get(column.key, result.inserted_primary_key[index])
                for index, column in enumerate(table.primary_key.columns)
            }
        except IntegrityError as error:
            self.db.rollback()
            raise RecordConflictError(
                "The record conflicts with existing data"
            ) from error
        record = self._get_record(table, key_values)
        if record is None:
            raise RecordNotFoundError("Inserted record could not be reloaded")
        return self._record_for(table, record)

    def update(
        self, resource: str, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        table = self._table_for(resource)
        self._validate_fields(table, data, updating=True)
        key_values = self._parse_key(table, record_id)
        conditions = self._key_conditions(table, key_values)
        try:
            result = self.db.execute(
                update(table).where(and_(*conditions)).values(**data)
            )
            if result.rowcount == 0:
                self.db.rollback()
                raise RecordNotFoundError(record_id)
            self.db.commit()
        except IntegrityError as error:
            self.db.rollback()
            raise RecordConflictError(
                "The update conflicts with existing data"
            ) from error
        record = self._get_record(table, key_values)
        if record is None:
            raise RecordNotFoundError(record_id)
        return self._record_for(table, record)

    def delete(self, resource: str, record_id: str) -> None:
        table = self._table_for(resource)
        key_values = self._parse_key(table, record_id)
        try:
            result = self.db.execute(
                delete(table).where(
                    and_(*self._key_conditions(table, key_values))
                )
            )
            if result.rowcount == 0:
                self.db.rollback()
                raise RecordNotFoundError(record_id)
            self.db.commit()
        except IntegrityError as error:
            self.db.rollback()
            raise RecordConflictError(
                "The record cannot be deleted while it is referenced"
            ) from error

    def delete_all(self, resource: str) -> int:
        table = self._table_for(resource)
        try:
            result = self.db.execute(delete(table))
            self.db.commit()
            return result.rowcount
        except IntegrityError as error:
            self.db.rollback()
            raise RecordConflictError(
                "Some records cannot be deleted while referenced"
            ) from error