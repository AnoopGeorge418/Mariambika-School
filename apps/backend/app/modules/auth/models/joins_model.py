import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.base import Base

if TYPE_CHECKING:
    from app.modules.auth.models.admins_model import Admins
    from app.modules.auth.models.permissions_model import Permissions


# For many to many relationship - many admins can have many permission
class AdminPermission(Base):
    __tablename__ = "admin_permissions"

    admin_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("admins.id"), nullable=False, primary_key=True
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("permissions.id"), nullable=False, primary_key=True
    )

    assigned_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )

    assigned_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("admins.id"), nullable=True
    )

    admin: Mapped["Admins"] = relationship(
        foreign_keys=[admin_id], back_populates="admin_permissions"
    )
    permission: Mapped["Permissions"] = relationship(foreign_keys=[permission_id])
    assigned_by_admin: Mapped["Admins | None"] = relationship(
        foreign_keys=[assigned_by]
    )
