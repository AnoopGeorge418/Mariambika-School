"""${message}

Revision ID: f1c8babcbcc7
Revises: 095caf5052cb
Create Date: 2026-09-04 13:27:16.895700

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1c8babcbcc7"
down_revision: str | Sequence[str] | None = "095caf5052cb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    resources_enum = postgresql.ENUM(
        "ADMINS",
        "STUDENTS",
        "TEACHERS",
        "FINANCE",
        "TRANSPORT",
        "SETTINGS",
        name="resources",
    )
    resources_enum.create(bind, checkfirst=True)

    authpermissions_enum = postgresql.ENUM(
        "READ",
        "WRITE",
        "UPDATE",
        "DELETE",
        name="authpermissions",
    )
    authpermissions_enum.create(bind, checkfirst=True)

    op.alter_column(
        "admin_permissions", "assigned_by", existing_type=sa.UUID(), nullable=True
    )
    op.add_column("permissions", sa.Column("resource", resources_enum, nullable=False))
    op.add_column(
        "permissions", sa.Column("action", authpermissions_enum, nullable=False)
    )
    op.create_unique_constraint(
        "uq_permission_resource_action", "permissions", ["resource", "action"]
    )
    op.drop_column("permissions", "name")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "permissions",
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("uq_permission_resource_action", "permissions", type_="unique")
    op.drop_column("permissions", "action")
    op.drop_column("permissions", "resource")
    op.alter_column(
        "admin_permissions", "assigned_by", existing_type=sa.UUID(), nullable=False
    )

    bind = op.get_bind()
    postgresql.ENUM(name="authpermissions").drop(bind, checkfirst=True)
    postgresql.ENUM(name="resources").drop(bind, checkfirst=True)
