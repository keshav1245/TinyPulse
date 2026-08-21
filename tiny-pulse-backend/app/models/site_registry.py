"""Website model"""

from app.db.base import Base
from datetime import datetime
from uuid import uuid4

from sqlalchemy import func, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column


class Website(Base):
    """Model for storing website data"""

    __tablename__ = "websites"

    # Primary Key
    site_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )

    url: Mapped[str] = mapped_column(String(256), nullable=False)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    check_interval: Mapped[int] = mapped_column(Integer, nullable=False, default=180)

    is_active: Mapped[Boolean] = mapped_column(Boolean, nullable=False, default=True)

    date_created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp()
    )

    date_modified: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    def __repr__(self) -> str:
        return f"<Website(site_id={self.site_id}, url={self.url}, name={self.name})>"

