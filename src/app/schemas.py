from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class SignupRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("invalid email")
        return value.lower()


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("invalid email")
        return value.lower()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class WishCreate(BaseModel):
    title: str
    link: Optional[str] = Field(default=None, max_length=255)
    price_estimate: Optional[Decimal] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator("price_estimate", mode="before")
    @classmethod
    def normalize_price(cls, value):
        if value is None:
            return value
        quantized = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if quantized < 0:
            raise ValueError("price must be >= 0")
        return quantized


class WishUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = Field(default=None, max_length=255)
    price_estimate: Optional[Decimal] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    status: Optional[str] = None

    @field_validator("price_estimate", mode="before")
    @classmethod
    def normalize_price(cls, value):
        if value is None:
            return value
        quantized = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if quantized < 0:
            raise ValueError("price must be >= 0")
        return quantized


class WishResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    link: Optional[str] = None
    price_estimate: Optional[str] = None
    notes: Optional[str] = None
    priority: int
    status: str
    archived: bool
    attachments: List[str]


class AttachmentUpload(BaseModel):
    content_base64: str


class WishListResponse(BaseModel):
    total: int
    items: list[WishResponse]
