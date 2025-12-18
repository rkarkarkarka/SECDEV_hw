from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    role: UserRole = UserRole.USER
    created_at: datetime = field(default_factory=datetime.utcnow)


class WishStatus(str, Enum):
    ACTIVE = "active"
    PURCHASED = "purchased"
    ARCHIVED = "archived"


@dataclass
class Wish:
    id: int
    owner_id: int
    title: str
    link: Optional[str] = None
    price_estimate: Optional[Decimal] = None
    notes: Optional[str] = None
    priority: int = 1
    status: WishStatus = WishStatus.ACTIVE
    archived: bool = False
    attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update_timestamp(self) -> None:
        self.updated_at = datetime.utcnow()
