from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.auth.models.session_model import Session


class RefreshTokenRepo:
    @staticmethod
    async def get_session_token(session: AsyncSession, hashed_token) -> Session | None:
        """Returns token info if token found in database."""

        statement = (
            select(Session)
            .options(selectinload(Session.admin))
            .where(Session.hashed_refresh_token == hashed_token)
        )
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def flag_token_expired(
        session: AsyncSession, session_record: Session
    ) -> None:
        """Flags a session's refresh token as expired."""

        session_record.is_expired = True
        await session.commit()

    @staticmethod
    async def save_new_hashed_token(session: AsyncSession, payload: dict[str, Any]):
        """Saves new hashed into Session table and replaces old token."""

        new_session_record = Session(
            admin_id=payload["admin_id"],
            hashed_refresh_token=payload["new_token"],
            expires_at=payload["expires_at"],
            is_expired=payload["is_expired"],
            user_agent=payload["user_agent"],
            ip_address=payload["ip_address"],
            device_type=payload["device_type"],
        )

        session.add(new_session_record)
        await session.commit()
        await session.refresh(Session)
