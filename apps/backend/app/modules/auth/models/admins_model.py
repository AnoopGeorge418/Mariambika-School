import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.util.typing import final

from app.core.database.base import Base


@final
class Admins(Base):
    """Contains Metadata related admins model to create admin table in database."""

    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
