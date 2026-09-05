from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.dependency import get_db
from app.modules.auth.schemas.login_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
)

login_route = APIRouter(prefix="/login", tags=["Authentication and Authorization"])


@login_route.post(
    "/", status_code=status.HTTP_200_OK, response_model=LoginResponseSchema
)
async def get_user(
    payload: LoginRequestSchema, session: Annotated[AsyncSession, Depends(get_db)]
):
    """Validates user credentials and logs user in if correct."""
