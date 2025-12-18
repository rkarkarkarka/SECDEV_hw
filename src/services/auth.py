from __future__ import annotations

from src.adapters.memory import InMemoryDB, serialize_user
from src.domain import models
from src.shared import errors, security


class AuthService:
    def __init__(self, db: InMemoryDB):
        self.db = db

    def register_user(
        self, email: str, password: str, role: models.UserRole = models.UserRole.USER
    ) -> dict:
        if self.db.get_user_by_email(email):
            raise errors.ValidationError(message="email already registered")
        password_hash = security.hash_password(password)
        user = self.db.create_user(email=email, password_hash=password_hash, role=role)
        return serialize_user(user)

    def login(self, email: str, password: str) -> dict:
        user = self.db.get_user_by_email(email)
        if not user or not security.verify_password(password, user.password_hash):
            raise errors.AuthError(message="invalid credentials")
        token = security.generate_token()
        self.db.store_token(token, user.id)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": serialize_user(user),
        }

    def logout(self, token: str) -> None:
        self.db.revoke_token(token)

    def get_user_from_token(self, token: str) -> models.User:
        user_id = self.db.get_user_id_by_token(token)
        if not user_id:
            raise errors.AuthError(message="invalid or expired token")
        user = self.db.get_user(user_id)
        if not user:
            raise errors.AuthError(message="user no longer exists")
        return user
