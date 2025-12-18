from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from starlette.responses import JSONResponse

from src.shared import context


class DomainError(Exception):
    """Base class for predictable errors inside the domain/services."""

    code = "domain_error"
    title = "Domain error"
    detail = "Domain error"
    status = 400
    extras: Dict[str, Any] | None = None

    def __init__(
        self,
        detail: Optional[str] = None,
        *,
        status: Optional[int] = None,
        extras: Optional[Dict[str, Any]] = None,
    ):
        if detail:
            self.detail = detail
        if status:
            self.status = status
        self.extras = extras or {}

    def to_problem(self) -> JSONResponse:
        return problem_response(
            status=self.status,
            title=self.title,
            detail=self.detail,
            type_=f"https://wishlist.example/errors/{self.code}",
            extras={"code": self.code, **self.extras},
        )


class ValidationError(DomainError):
    code = "validation_error"
    title = "Validation error"
    detail = "Payload validation failed"
    status = 422


class AuthError(DomainError):
    code = "auth_error"
    title = "Authentication error"
    detail = "Authentication failed"
    status = 401


class TooManyRequestsError(DomainError):
    code = "too_many_attempts"
    title = "Too many attempts"
    detail = "Too many requests"
    status = 429


class NotFoundError(DomainError):
    code = "not_found"
    title = "Not found"
    detail = "Resource not found"
    status = 404


class ForbiddenError(DomainError):
    code = "forbidden"
    title = "Forbidden"
    detail = "Action is not allowed"
    status = 403


def problem_response(
    *,
    status: int,
    title: str,
    detail: str,
    type_: str = "about:blank",
    extras: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    correlation_id = context.get_request_id() or str(uuid4())
    payload: Dict[str, Any] = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": correlation_id,
    }
    if extras:
        payload.update(extras)
    response = JSONResponse(payload, status_code=status)
    response.headers["X-Request-ID"] = correlation_id
    return response
