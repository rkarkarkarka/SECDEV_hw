from __future__ import annotations

from typing import Optional

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
    price_estimate: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    priority: int = Field(default=1, ge=1, le=5)


class WishUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = Field(default=None, max_length=255)
    price_estimate: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    status: Optional[str] = None


class WishResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    link: Optional[str] = None
    price_estimate: Optional[float] = None
    notes: Optional[str] = None
    priority: int
    status: str
    archived: bool


class WishListResponse(BaseModel):
    total: int
    items: list[WishResponse]
