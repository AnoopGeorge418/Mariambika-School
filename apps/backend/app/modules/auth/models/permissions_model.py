import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, Enum, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util.typing import final

from app.core.database.base import Base
from app.modules.auth.enums.auth_permission_enum import AuthPermissions, Resources

if TYPE_CHECKING:
    from app.modules.auth.models.joins_model import AdminPermission


@final
class Permissions(Base):
    """Model contains Permissions information allowed to each admin"""

    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint("resource", "action", name="uq_permission_resource_action"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    resource: Mapped[Resources] = mapped_column(Enum(Resources), nullable=False)
    action: Mapped[AuthPermissions] = mapped_column(
        Enum(AuthPermissions), nullable=False
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        insert_default=func.now(),
        server_default=func.now(),
    )

    admin: Mapped[list["AdminPermission"]] = relationship(back_populates="permission")

    def __str__(self) -> str:
        return f"{self.resource.value}:{self.action.value}"
