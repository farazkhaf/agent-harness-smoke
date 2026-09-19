"""Stable API-facing error dictionaries."""

from __future__ import annotations

from typing import Any


def error_payload(code: str, message: str, *, detail: dict[str, Any] | None = None) -> dict[str, Any]:
    if not code.strip():
        raise ValueError("error code cannot be empty")
    if not message.strip():
        raise ValueError("error message cannot be empty")
    payload: dict[str, Any] = {"error": {"code": code, "message": message}}
    if detail:
        payload["error"]["detail"] = detail
    return payload
