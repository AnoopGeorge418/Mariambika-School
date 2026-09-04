from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.enums.auth_permission_enum import AuthPermissions, Resources
from app.modules.auth.models.permissions_model import Permissions


class PermissionsRepo:
    @staticmethod
    async def seed_permissions(session: AsyncSession) -> int:
        """
        Ensures a Permissions row exists for every (resource, action) pair.
        Idempotent: safe to run multiple times, existing rows are left untouched.
        Returns the number of rows in the catalog after seeding.
        """

        rows = [
            {"resource": resource, "action": action}
            for resource in Resources
            for action in AuthPermissions
        ]

        stmt = pg_insert(Permissions).values(rows)
        stmt = stmt.on_conflict_do_nothing(constraint="uq_permission_resource_action")

        await session.execute(stmt)
        await session.commit()

        result = await session.scalars(select(Permissions.id))
        return len(list(result.all()))
