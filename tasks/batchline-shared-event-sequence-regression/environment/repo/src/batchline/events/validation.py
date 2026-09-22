"""JSON Schema loading and event validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


DEFAULT_SCHEMA = Path(__file__).resolve().parents[3] / "schemas" / "events.schema.json"


class EventValidationError(ValueError):
    pass


def load_event_schema(path: Path | str = DEFAULT_SCHEMA) -> dict[str, Any]:
    schema_path = Path(path)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def make_validator(path: Path | str = DEFAULT_SCHEMA) -> Draft202012Validator:
    schema = load_event_schema(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_event(event: Mapping[str, Any], *, schema_path: Path | str = DEFAULT_SCHEMA) -> None:
    validator = make_validator(schema_path)
    try:
        validator.validate(dict(event))
    except ValidationError as exc:
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        raise EventValidationError(f"{location}: {exc.message}") from exc


def validation_errors(event: Mapping[str, Any], *, schema_path: Path | str = DEFAULT_SCHEMA) -> tuple[str, ...]:
    validator = make_validator(schema_path)
    errors = []
    for exc in sorted(validator.iter_errors(dict(event)), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        errors.append(f"{location}: {exc.message}")
    return tuple(errors)


def schema_event_types(*, schema_path: Path | str = DEFAULT_SCHEMA) -> tuple[str, ...]:
    """Return event type constants represented by concrete schema definitions."""
    schema = load_event_schema(schema_path)
    names: list[str] = []
    for definition in schema.get("$defs", {}).values():
        if not isinstance(definition, dict):
            continue
        event_type = definition.get("properties", {}).get("event_type", {})
        if isinstance(event_type, dict) and isinstance(event_type.get("const"), str):
            names.append(event_type["const"])
    return tuple(sorted(names))


def registry_schema_errors(*, schema_path: Path | str = DEFAULT_SCHEMA) -> tuple[str, ...]:
    """Report drift between the event registry and concrete schema variants."""
    from .registry import event_types

    registered = {item.name for item in event_types()}
    schema_names = set(schema_event_types(schema_path=schema_path))
    errors: list[str] = []
    for name in sorted(registered - schema_names):
        errors.append(f"registered event missing from schema: {name}")
    for name in sorted(schema_names - registered):
        errors.append(f"schema event missing from registry: {name}")
    return tuple(errors)
