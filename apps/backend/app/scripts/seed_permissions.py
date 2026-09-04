import asyncio

from app.core.database.async_session import AsyncLocalSession
from app.core.log.logger import CustomAppLogger
from app.modules.auth.repositories.permissions_repo import PermissionsRepo


async def main() -> None:
    """
    Seeds the permissions catalog (one row per Resources x AuthPermissions pair).
    Idempotent - safe to re-run.
    command: uv run -m app.scripts.seed_permissions

    Must be run BEFORE app.scripts.create_super_admin, which requires the
    full permissions catalog to already exist.
    """

    async with AsyncLocalSession() as db:
        logger = CustomAppLogger()
        log = logger.get_logger()

        log.warning("Seeding permissions catalog!")
        total = await PermissionsRepo.seed_permissions(db)
        log.warning(f"Permissions catalog seeded successfully! ({total} rows)")


if __name__ == "__main__":
    asyncio.run(main())
