import os
from pathlib import Path
from typing import final

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repositories.super_admin_repo import SuperAdminRepo


@final
class CreateSuperAdmin:
    """
    Creates first super admin in database.
    if super admin already exists, abort.
    One-time creation only.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.BASE_DIR = Path(__file__).resolve().parents[4]

        load_dotenv(dotenv_path=self.BASE_DIR / ".env")

        self.email: str = self._required_env("MARIAMBIKA_SUPER_ADMIN_EMAIL")
        self.username: str = self._required_env("MARIAMBIKA_SUPER_ADMIN_USERNAME")
        self.password: str = self._required_env("MARIAMBIKA_SUPER_ADMIN_PASSWORD")

    @staticmethod
    def _required_env(name: str) -> str:
        value = os.getenv(name)

        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")

        return value

    async def check_super_admin(self):
        """Returns True if a SUPER_ADMIN already exists"""

        return await SuperAdminRepo.check_super_admin(self.db)

    async def create_super_admin(self):
        """Creates SUPER_ADMIN only if one does not already exist."""

        if await self.check_super_admin():
            raise RuntimeError("SUPER_ADMIN already exists. Bootstrap aborted.")

        # create super admin
