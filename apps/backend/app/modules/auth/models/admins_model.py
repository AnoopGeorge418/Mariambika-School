import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util.typing import final

from app.core.database.base import Base
from app.modules.auth.enums.auth_permission_enum import AuthPermissions, Resources
from app.modules.auth.enums.auth_roles_enum import AuthRoles
from app.modules.auth.models.otp_model import Otp

if TYPE_CHECKING:
    from app.modules.auth.models.joins_model import AdminPermission
    from app.modules.auth.models.session_model import Sessions


@final
class Admins(Base):
    """Contains Metadata related admins model to create admin table in database."""

    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String, index=True, nullable=False, unique=True
    )

    firstname: Mapped[str] = mapped_column(String, nullable=False)

    lastname: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, index=True, nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[AuthRoles] = mapped_column(Enum(AuthRoles), nullable=False)

    # if logged in true else false
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # if email verified true else false
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    last_login: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        insert_default=func.now(),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        insert_default=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    permission: Mapped[list["AdminPermission"]] = relationship(
        foreign_keys="[AdminPermission.admin_id]", back_populates="admins"
    )
    sessions: Mapped[list["Sessions"]] = relationship(
        back_populates="admin", cascade="all, delete-orphan"
    )
    otp: Mapped[list["Otp"]] = relationship(
        back_populates="admin", cascade="all, delete-orphan"
    )

    def has_permission(self, resource: Resources, action: AuthPermissions) -> bool:
        """Super admin bypasses explicit grants; everyone else needs a matching row."""

        if self.role == AuthRoles.SUPER_ADMIN:
            return True
        return any(
            link.permission.resource == resource and link.permission.action == action
            for link in self.permission
        )
