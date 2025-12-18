from __future__ import annotations

from typing import Optional


class DomainError(Exception):
    """Base class for predictable errors inside the domain/services."""

    code = "domain_error"
    message = "Domain error"
    status = 400
    details: Optional[dict] = None

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        status: Optional[int] = None,
        details: Optional[dict] = None,
    ):
        if message:
            self.message = message
        if status:
            self.status = status
        if details is not None:
            self.details = details
        else:
            self.details = self.details or {}

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details or {},
        }


class ValidationError(DomainError):
    code = "validation_error"
    message = "Payload validation failed"
    status = 422


class AuthError(DomainError):
    code = "auth_error"
    message = "Authentication failed"
    status = 401


class NotFoundError(DomainError):
    code = "not_found"
    message = "Resource not found"
    status = 404


class ForbiddenError(DomainError):
    code = "forbidden"
    message = "Action is not allowed"
    status = 403
