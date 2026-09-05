import datetime

from fastapi import HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from user_agents import parse  # type: ignore[import-untyped]

from app.core.config.settings import APP_SETTINGS
from app.core.security.token_handler import TokenHandlerSecurity
from app.modules.auth.repositories.refresh_repo import RefreshTokenRepo
from app.modules.auth.schemas.refresh_schema import (
    HeaderMetaData,
    RefreshTokenResponseSchema,
)


class RefreshTokenService:
    """
    Responsible for fast user/admin authentication and login based on tokens
    If available - rotates new tokens and logs in
    If not available - flags False
    """

    @staticmethod
    def fetch_meta_data(request: Request) -> HeaderMetaData:
        """Fetches headers like user-agent, ip-address and device type from request"""

        user_agent = request.headers.get("user-agent", "Unknown")
        ip_address = request.client.host if request.client else "Unknown"

        # device type
        parsed_user_agent = parse(user_agent)
        if parsed_user_agent.is_mobile:
            device_type = "Mobile"
        elif parsed_user_agent.is_tablet:
            device_type = "Tablet"
        else:
            device_type = "Desktop"

        return HeaderMetaData(
            user_agent=user_agent,
            ip_address=ip_address,
            device_type=device_type,
        )

    @staticmethod
    async def handle_refresh_auth(
        request: Request,
        response: Response,
        session: AsyncSession,
        data: HeaderMetaData,
    ):
        """
        Fetches refresh token from request and validates it for auto login.
        Returns Rotated Access and refresh tokens
        """

        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No Refresh Token Found!",  # in cookies
            )  # frontend redirects to /login route

        # hashing refresh token using hmac
        token_handler = TokenHandlerSecurity()
        hashed_token = token_handler.hash_refresh_token(refresh_token)

        # checks if token in db
        session_record = await RefreshTokenRepo.get_session_token(
            session, hashed_token=hashed_token
        )
        if not session_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No Session Found!",  # in db
            )  # frontend redirects to /login route

        # verify raw refresh token against hashed token
        verified_token = token_handler.verify_hashed_refresh_token(
            raw_token=refresh_token, stored_hash=session_record.hashed_refresh_token
        )
        if not verified_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No Session Found!",  # in db
            )  # frontend redirects to /login route

        # check expired or not
        now = datetime.datetime.now(datetime.UTC)
        expiry_moment = session_record.created_at + datetime.timedelta(
            seconds=session_record.expires_at
        )
        if expiry_moment < now:
            # flag session expired
            await RefreshTokenRepo.flag_token_expired(session, session_record)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired. Please log in again.",
            )  # frontend redirects to /login route

        # Issue new refresh and access tokens
        new_refresh_token = token_handler.create_refresh_token()
        hashed_new_token = token_handler.hash_refresh_token(new_refresh_token)

        # add new hashed token into db -- refresh token rotation
        payload = {
            "admin_id": session_record.admin_id,
            "new_token": hashed_new_token,
            "expires_at": APP_SETTINGS.REFRESH_TOKEN_EXPIRES_AT,
            "is_expired": False,
            "user_agent": data.user_agent,
            "ip_address": data.ip_address,
            "device_type": data.device_type,
        }
        await RefreshTokenRepo.save_new_hashed_token(session, payload)

        # generate new access token
        access_token, expires_in = token_handler.create_access_token(
            admin_id=session_record.admin_id, roles=session_record.admin.role
        )

        # storing refresh token in cookies
        cookie_config = APP_SETTINGS.switch_cookies_set_based_on_env
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=APP_SETTINGS.REFRESH_TOKEN_EXPIRES_AT,
            path="/auth/refresh",
            secure=cookie_config.secure,
            httponly=True,
            samesite=cookie_config.samesite,  # cross-site: vercal, render
        )

        # return access token and expires in
        return RefreshTokenResponseSchema(
            access_token=access_token, expires_in=expires_in
        )
