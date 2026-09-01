import asyncio

from app.core.database.async_session import AsyncLocalSession
from app.core.log.logger import CustomAppLogger
from app.modules.auth.services.super_admin_script import CreateSuperAdmin


async def main() -> None:
    """
    Creates super admin only once if not exists in db
    command: uv run -m app.scripts.create_super_admin
    """

    async with AsyncLocalSession() as db:
        logger = CustomAppLogger()
        log = logger.get_logger()

        creator = CreateSuperAdmin(db=db)

        log.warning("Attempting to create super admin!")
        await creator.create_super_admin()
        log.warning("Super admin created successfully!")


if __name__ == "__main__":
    asyncio.run(main())
