from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.dependency import get_db
from app.modules.auth.schemas.login_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
)
from app.modules.auth.schemas.refresh_schema import RefreshTokenResponseSchema

auth_route = APIRouter(prefix="/auth", tags=["Authentication and Authorization"])


@auth_route.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=RefreshTokenResponseSchema,
)
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )

    # 1. Validate refresh token
    # 2. Find session/token in DB
    # 3. Check expiration/revocation
    # 4. Rotate refresh token
    # 5. Generate new access token
    # 6. Set new refresh token cookie

    # return access_token and expires_in


@auth_route.post(
    "/login", status_code=status.HTTP_200_OK, response_model=LoginResponseSchema
)
async def get_user(
    payload: LoginRequestSchema, session: Annotated[AsyncSession, Depends(get_db)]
):
    """Validates user credentials and logs user in if correct."""
