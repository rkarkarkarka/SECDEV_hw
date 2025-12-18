from __future__ import annotations

import os
from typing import Optional

from fastapi import Depends, Header

from src.adapters.memory import InMemoryDB
from src.domain import models
from src.services.auth import AuthService
from src.services.wishes import WishService
from src.shared import errors

_db = InMemoryDB()
_auth_service = AuthService(_db)
_wish_service = WishService(_db)

ADMIN_EMAIL = os.getenv("APP_ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("APP_ADMIN_PASSWORD", "ChangeMe123!")


def _seed_admin() -> None:
    if not _db.get_user_by_email(ADMIN_EMAIL):
        _auth_service.register_user(
            email=ADMIN_EMAIL, password=ADMIN_PASSWORD, role=models.UserRole.ADMIN
        )


def get_auth_service() -> AuthService:
    return _auth_service


def get_wish_service() -> WishService:
    return _wish_service


def get_bearer_token(
    authorization: Optional[str] = Header(default=None, alias="Authorization")
) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise errors.AuthError(detail="missing bearer token")
    return authorization.split(" ", 1)[1]


def get_current_user(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> models.User:
    return auth_service.get_user_from_token(token)


def reset_state() -> None:
    _db.reset()
    _seed_admin()


_seed_admin()
