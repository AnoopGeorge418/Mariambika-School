import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util.typing import final

from app.core.database.base import Base

if TYPE_CHECKING:
    from app.modules.auth.models.admins_model import Admins


@final
class Session(Base):
    """Model contains session tokens metadata"""

    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("admins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    hashed_refresh_token: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )

    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)

    is_expired: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )  # True if expired

    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    device_type: Mapped[str | None] = mapped_column(String, nullable=True)

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

    admin: Mapped["Admins"] = relationship(back_populates="sessions")
