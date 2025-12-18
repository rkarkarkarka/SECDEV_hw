from __future__ import annotations

import os
from datetime import datetime, timedelta

from src.adapters.memory import InMemoryDB, serialize_user
from src.domain import models
from src.shared import errors, security
from src.shared.rate_limiter import RateLimiter

LOGIN_RATE_LIMIT = int(os.getenv("APP_LOGIN_RATE_LIMIT", "5"))
LOGIN_RATE_WINDOW = int(os.getenv("APP_LOGIN_RATE_WINDOW", "60"))
TOKEN_TTL_SECONDS = int(os.getenv("APP_TOKEN_TTL_SECONDS", "900"))


class AuthService:
    def __init__(self, db: InMemoryDB):
        self.db = db
        self.login_rate_limiter = RateLimiter(
            limit=LOGIN_RATE_LIMIT, window_seconds=LOGIN_RATE_WINDOW
        )

    def register_user(
        self, email: str, password: str, role: models.UserRole = models.UserRole.USER
    ) -> dict:
        if self.db.get_user_by_email(email):
            raise errors.ValidationError(detail="email already registered")
        password_hash = security.hash_password(password)
        user = self.db.create_user(email=email, password_hash=password_hash, role=role)
        return serialize_user(user)

    def login(self, email: str, password: str) -> dict:
        key = email.lower()
        if self.login_rate_limiter.is_blocked(key):
            raise errors.TooManyRequestsError(
                detail="too many login attempts, try again later"
            )
        user = self.db.get_user_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            self.login_rate_limiter.hit(key)
            raise errors.AuthError(detail="invalid credentials")
        self.login_rate_limiter.reset(key)
        token = security.generate_token()
        self.db.store_token(token, user.id, datetime.utcnow())
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": serialize_user(user),
        }

    def logout(self, token: str) -> None:
        self.db.revoke_token(token)

    def get_user_from_token(self, token: str) -> models.User:
        token_data = self.db.get_token(token)
        if not token_data:
            raise errors.AuthError(detail="invalid or expired token")
        issued_at = token_data["issued_at"]
        if isinstance(
            issued_at, datetime
        ) and datetime.utcnow() - issued_at > timedelta(seconds=TOKEN_TTL_SECONDS):
            self.db.revoke_token(token)
            raise errors.AuthError(detail="invalid or expired token")
        user = self.db.get_user(int(token_data["user_id"]))
        if not user:
            raise errors.AuthError(detail="user no longer exists")
        return user
