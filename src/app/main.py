from __future__ import annotations

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import JSONResponse
from starlette import status

from src.app import schemas
from src.app.dependencies import (
    get_auth_service,
    get_bearer_token,
    get_current_user,
    get_wish_service,
)
from src.domain import models
from src.services.auth import AuthService
from src.services.wishes import WishService
from src.shared import errors

app = FastAPI(title="Wishlist API", version="0.1.0")


@app.exception_handler(errors.DomainError)
async def handle_domain_error(request: Request, exc: errors.DomainError):
    return JSONResponse(status_code=exc.status, content={"error": exc.to_dict()})


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "internal_error",
                "message": "unexpected error",
                "details": {},
            }
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/auth/signup")
async def signup(
    data: schemas.SignupRequest, auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.register_user(email=data.email, password=data.password)
    return {"user": user}


@app.post("/api/v1/auth/login", response_model=schemas.TokenResponse)
async def login(
    data: schemas.LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login(email=data.email, password=data.password)


@app.post("/api/v1/auth/logout")
async def logout(
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_service.logout(token)
    return {"status": "logged_out"}


@app.get("/api/v1/wishes", response_model=schemas.WishListResponse)
async def list_wishes(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: models.User = Depends(get_current_user),
    wish_service: WishService = Depends(get_wish_service),
):
    return wish_service.list_wishes(
        owner_id=current_user.id, limit=limit, offset=offset
    )


@app.post(
    "/api/v1/wishes",
    response_model=schemas.WishResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wish(
    payload: schemas.WishCreate,
    current_user: models.User = Depends(get_current_user),
    wish_service: WishService = Depends(get_wish_service),
):
    return wish_service.create_wish(
        owner_id=current_user.id,
        title=payload.title,
        link=payload.link,
        price=payload.price_estimate,
        notes=payload.notes,
        priority=payload.priority,
    )


@app.get("/api/v1/wishes/{wish_id}", response_model=schemas.WishResponse)
async def get_wish(
    wish_id: int,
    current_user: models.User = Depends(get_current_user),
    wish_service: WishService = Depends(get_wish_service),
):
    return wish_service.get_wish(
        owner_id=current_user.id,
        wish_id=wish_id,
        is_admin=current_user.role == models.UserRole.ADMIN,
    )


@app.patch("/api/v1/wishes/{wish_id}", response_model=schemas.WishResponse)
async def patch_wish(
    wish_id: int,
    payload: schemas.WishUpdate,
    current_user: models.User = Depends(get_current_user),
    wish_service: WishService = Depends(get_wish_service),
):
    update_data = payload.model_dump(exclude_unset=True)
    return wish_service.update_wish(
        owner_id=current_user.id,
        wish_id=wish_id,
        is_admin=current_user.role == models.UserRole.ADMIN,
        data=update_data,
    )


@app.delete("/api/v1/wishes/{wish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wish(
    wish_id: int,
    current_user: models.User = Depends(get_current_user),
    wish_service: WishService = Depends(get_wish_service),
):
    wish_service.delete_wish(
        owner_id=current_user.id,
        wish_id=wish_id,
        is_admin=current_user.role == models.UserRole.ADMIN,
    )
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
