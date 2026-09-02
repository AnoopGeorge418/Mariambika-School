import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.util.typing import final

from app.core.database.base import Base


@final
class Roles(Base):
    """Model contains roles information for each admin"""

    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
