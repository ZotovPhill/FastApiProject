from fastapi import APIRouter

from app.core.settings import settings
from app.orm.schemas.request.security.auth_request import (
    OAuth2PasswordRequest,
    OAuth2RefreshTokenRequest,
)
from app.orm.schemas.response.security.auth_response import Token
from app.services.security.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(data: OAuth2PasswordRequest):
    user = await authenticate_user(data.email, data.password)
    access_token, refresh_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh_access_token(data: OAuth2RefreshTokenRequest):
    user = await get_current_user(data.refresh_token)
    access_token, refresh_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, refresh_token=refresh_token) \
        if settings.new_refresh_on_update \
        else Token(access_token=access_token).dict(exclude_none=True)
