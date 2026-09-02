import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.util.typing import final

from app.core.database.base import Base


@final
class Permissions(Base):
    """Model contains Permissions information allowed to each admin"""

    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
