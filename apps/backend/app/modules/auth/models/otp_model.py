import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.util.typing import final

from app.core.database.base import Base
from app.modules.auth.enums.otp_purpose_enum import OtpPurpose

if TYPE_CHECKING:
    from app.modules.auth.models.admins_model import Admins


@final
class Otp(Base):
    """Model contains otp metadata"""

    __tablename__ = "otp"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )

    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("admins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    hashed_otp: Mapped[str] = mapped_column(String, nullable=False)
    purpose: Mapped[OtpPurpose] = mapped_column(Enum(OtpPurpose), nullable=False)

    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    expires_in: Mapped[int] = mapped_column(Integer, nullable=False)

    max_retry_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    current_retry_attempt: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    max_resend_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    current_resend_attempt: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
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

    admin: Mapped["Admins"] = relationship(back_populates="otp")
