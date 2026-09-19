"""JSON Schema validation for raw Batchline service catalogs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


DEFAULT_SERVICE_SCHEMA = Path(__file__).resolve().parents[3] / "schemas" / "service-config.schema.json"


class ServiceConfigSchemaError(ValueError):
    """Raised when the raw service catalog does not satisfy its schema."""


def load_service_schema(path: Path | str = DEFAULT_SERVICE_SCHEMA) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_service_validator(path: Path | str = DEFAULT_SERVICE_SCHEMA) -> Draft202012Validator:
    schema = load_service_schema(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_service_document(
    document: Mapping[str, Any],
    *,
    schema_path: Path | str = DEFAULT_SERVICE_SCHEMA,
) -> None:
    validator = make_service_validator(schema_path)
    try:
        validator.validate(dict(document))
    except ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        raise ServiceConfigSchemaError(f"{location}: {exc.message}") from exc


def service_document_errors(
    document: Mapping[str, Any],
    *,
    schema_path: Path | str = DEFAULT_SERVICE_SCHEMA,
) -> tuple[str, ...]:
    validator = make_service_validator(schema_path)
    errors: list[str] = []
    for exc in sorted(validator.iter_errors(dict(document)), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        errors.append(f"{location}: {exc.message}")
    return tuple(errors)
