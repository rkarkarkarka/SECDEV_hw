from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Optional

from src.domain import models


class InMemoryDB:
    def __init__(self) -> None:
        self._user_id = 0
        self._wish_id = 0
        self.users: Dict[int, models.User] = {}
        self.wishes: Dict[int, models.Wish] = {}
        self.tokens: Dict[str, int] = {}

    def reset(self) -> None:
        self._user_id = 0
        self._wish_id = 0
        self.users.clear()
        self.wishes.clear()
        self.tokens.clear()

    # User operations
    def create_user(
        self, email: str, password_hash: str, role: models.UserRole
    ) -> models.User:
        self._user_id += 1
        user = models.User(
            id=self._user_id, email=email, password_hash=password_hash, role=role
        )
        self.users[user.id] = user
        return user

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return next((u for u in self.users.values() if u.email == email), None)

    def get_user(self, user_id: int) -> Optional[models.User]:
        return self.users.get(user_id)

    # Token operations
    def store_token(self, token: str, user_id: int) -> None:
        self.tokens[token] = user_id

    def revoke_token(self, token: str) -> None:
        self.tokens.pop(token, None)

    def get_user_id_by_token(self, token: str) -> Optional[int]:
        return self.tokens.get(token)

    # Wish operations
    def create_wish(self, wish: models.Wish) -> models.Wish:
        self._wish_id += 1
        wish.id = self._wish_id
        self.wishes[wish.id] = wish
        return wish

    def list_wishes_for_owner(self, owner_id: int) -> List[models.Wish]:
        return [
            w for w in self.wishes.values() if w.owner_id == owner_id and not w.archived
        ]

    def get_wish(self, wish_id: int) -> Optional[models.Wish]:
        return self.wishes.get(wish_id)

    def save_wish(self, wish: models.Wish) -> None:
        self.wishes[wish.id] = wish

    def delete_wish(self, wish_id: int) -> None:
        if wish_id in self.wishes:
            del self.wishes[wish_id]


def serialize_user(user: models.User) -> dict:
    data = asdict(user)
    data.pop("password_hash", None)
    return data
