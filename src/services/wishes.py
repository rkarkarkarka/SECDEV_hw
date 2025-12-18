from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from src.adapters.memory import InMemoryDB
from src.domain import models
from src.shared import errors


class WishService:
    def __init__(self, db: InMemoryDB):
        self.db = db

    def create_wish(
        self,
        owner_id: int,
        title: str,
        link: Optional[str],
        price: Optional[float],
        notes: Optional[str],
        priority: int,
    ) -> dict:
        self._validate_common_fields(
            title=title, link=link, price=price, notes=notes, priority=priority
        )
        wish = models.Wish(
            id=0,
            owner_id=owner_id,
            title=title,
            link=link,
            price_estimate=price,
            notes=notes,
            priority=priority,
        )
        stored = self.db.create_wish(wish)
        return self._serialize(stored)

    def list_wishes(self, owner_id: int, limit: int, offset: int) -> dict:
        if limit < 1 or limit > 100:
            raise errors.ValidationError(message="limit must be 1..100")
        if offset < 0:
            raise errors.ValidationError(message="offset must be >= 0")
        wishes = self.db.list_wishes_for_owner(owner_id)
        total = len(wishes)
        slice_ = wishes[offset : offset + limit]
        return {"total": total, "items": [self._serialize(w) for w in slice_]}

    def get_wish(self, owner_id: int, wish_id: int, is_admin: bool) -> dict:
        wish = self.db.get_wish(wish_id)
        if not wish or wish.archived or (wish.owner_id != owner_id and not is_admin):
            raise errors.NotFoundError(message="wish not found")
        return self._serialize(wish)

    def update_wish(
        self,
        owner_id: int,
        wish_id: int,
        is_admin: bool,
        data: dict,
    ) -> dict:
        wish = self.db.get_wish(wish_id)
        if not wish or wish.archived or (wish.owner_id != owner_id and not is_admin):
            raise errors.NotFoundError(message="wish not found")
        if "title" in data:
            title = data["title"]
            if not title:
                raise errors.ValidationError(message="title is required")
            wish.title = title
        if "priority" in data:
            priority = data["priority"]
            if priority < 1 or priority > 5:
                raise errors.ValidationError(message="priority must be 1..5")
            wish.priority = priority
        if "link" in data:
            link = data["link"]
            if link and len(link) > 255:
                raise errors.ValidationError(message="link too long")
            wish.link = link
        if "price_estimate" in data:
            price = data["price_estimate"]
            if price is not None and price < 0:
                raise errors.ValidationError(message="price must be >= 0")
            wish.price_estimate = price
        if "notes" in data:
            if data["notes"] and len(data["notes"]) > 500:
                raise errors.ValidationError(message="notes too long")
            wish.notes = data["notes"]
        if "status" in data:
            try:
                wish.status = models.WishStatus(data["status"])
            except ValueError as exc:
                raise errors.ValidationError(message="unknown status") from exc
        wish.update_timestamp()
        self.db.save_wish(wish)
        return self._serialize(wish)

    def delete_wish(self, owner_id: int, wish_id: int, is_admin: bool) -> None:
        wish = self.db.get_wish(wish_id)
        if not wish or wish.archived or (wish.owner_id != owner_id and not is_admin):
            raise errors.NotFoundError(message="wish not found")
        wish.archived = True
        wish.update_timestamp()
        self.db.save_wish(wish)

    def _serialize(self, wish: models.Wish) -> dict:
        data = asdict(wish)
        data["status"] = wish.status.value
        return data

    def _validate_common_fields(
        self,
        title: str,
        link: Optional[str],
        price: Optional[float],
        notes: Optional[str],
        priority: int,
    ) -> None:
        if not title or len(title) > 200:
            raise errors.ValidationError(message="title must be 1..200 chars")
        if link and len(link) > 255:
            raise errors.ValidationError(message="link too long")
        if notes and len(notes) > 500:
            raise errors.ValidationError(message="notes too long")
        if price is not None and price < 0:
            raise errors.ValidationError(message="price must be >= 0")
        if priority < 1 or priority > 5:
            raise errors.ValidationError(message="priority must be 1..5")
