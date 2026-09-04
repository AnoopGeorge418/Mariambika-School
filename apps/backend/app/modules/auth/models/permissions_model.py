import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util.typing import final

from app.core.database.base import Base

if TYPE_CHECKING:
    from app.modules.auth.models.joins_model import AdminPermission


@final
class Permissions(Base):
    """Model contains Permissions information allowed to each admin"""

    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        insert_default=func.now(),
        server_default=func.now(),
    )

    admin: Mapped[list["AdminPermission"]] = relationship(back_populates="permissions")
