from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.dependency import get_db
from app.modules.auth.schemas.refresh_schema import RefreshTokenResponseSchema
from app.modules.auth.services.refresh_token_service import RefreshTokenService

refresh_route = APIRouter(prefix="/refresh", tags=["Refresh Tokens"])


@refresh_route.post(
    "/", status_code=status.HTTP_200_OK, response_model=RefreshTokenResponseSchema
)
async def refresh_token(
    request: Request,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_db)],
):

    metadata = RefreshTokenService.fetch_meta_data(request)
    refresh_auth = await RefreshTokenService.handle_refresh_auth(
        request, response, session, metadata
    )

    return HTTPException(status_code=status.HTTP_200_OK, detail=refresh_auth)
