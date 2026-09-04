import uuid

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.enums.auth_permission_enum import AuthPermissions, Resources
from app.modules.auth.enums.auth_roles_enum import AuthRoles
from app.modules.auth.models.admins_model import Admins
from app.modules.auth.models.joins_model import AdminPermission
from app.modules.auth.models.permissions_model import Permissions
from app.modules.auth.schemas.admin_schema import AdminCreateSchema


class SuperAdminRepo:
    @staticmethod
    async def get_all_permission_ids(session: AsyncSession) -> list[uuid.UUID]:
        """Returns every seeded permission id. Raises if the catalog is incomplete."""
        result = await session.scalars(select(Permissions.id))
        all_ids = list(result.all())

        expected_count = len(Resources) * len(AuthPermissions)
        if len(all_ids) < expected_count:
            raise RuntimeError(
                "Permissions catalog is not fully seeded — run seed_permissions() first."
            )
        return all_ids

    @staticmethod
    async def get_super_admin(session: AsyncSession) -> bool:
        """
        Returns True if at least one SUPER_ADMIN exists,
        otherwise returns False.
        """

        # Check if admin table has a role = admin associated with id
        statement = select(exists().where(Admins.role == AuthRoles.SUPER_ADMIN))

        has_super_admin = await session.scalar(statement)

        return bool(has_super_admin)

    @staticmethod
    async def create_super_admin(
        session: AsyncSession, data: AdminCreateSchema
    ) -> Admins:
        """Creates Super Admin in admins table with role = super_admin"""

        admin = Admins(
            username=data.username,
            firstname=data.firstname,
            lastname=data.lastname,
            email=data.email,
            hashed_password=data.hashed_password,
            role=data.role,
            is_active=data.is_active,
            is_verified=data.is_verified,
        )
        session.add(admin)
        await session.flush()

        if data.permissions:
            session.add_all(
                AdminPermission(admin_id=admin.id, permission_id=pid, assigned_by=None)
                for pid in data.permissions
            )

        await session.commit()
        await session.refresh(admin)

        return admin
