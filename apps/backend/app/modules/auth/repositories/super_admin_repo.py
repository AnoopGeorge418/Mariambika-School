from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models.admins_model import Admins


class SuperAdminRepo:
    @staticmethod
    async def get_super_admin(session: AsyncSession) -> bool:
        """
        Returns True if at least one SUPER_ADMIN exists,
        otherwise returns False.
        """

        # Check if admin table has a role = admin associated with id
        statement = select(exists().where(Admins.role == "super_admin"))

        has_super_admin = await session.scalar(statement)

        return bool(has_super_admin)

    async def create_super_admin(self, session: AsyncSession) -> bool:
        """Creates Super Admin in admins table with role = super_admin"""

        return False
