from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.async_session import AsyncLocalSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database dependency - yields an async session per request."""

    async with AsyncLocalSession() as async_local_session:
        yield async_local_session
