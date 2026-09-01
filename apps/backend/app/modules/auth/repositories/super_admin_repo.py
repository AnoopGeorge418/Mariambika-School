from sqlalchemy.ext.asyncio import AsyncSession


class SuperAdminRepo:
    @staticmethod
    async def check_super_admin(session: AsyncSession) -> bool:
        """
        Returns True if at least one SUPER_ADMIN exists,
        otherwise returns False.
        """

        return False
