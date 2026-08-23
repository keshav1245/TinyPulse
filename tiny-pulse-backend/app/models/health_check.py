"""Health check model - records the outcome of each site probe"""

from datetime import datetime
from uuid import uuid4

from app.db.base import Base
from app.models.enums import SiteStatus

from sqlalchemy import func, String, Integer, Boolean, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column


class HealthCheck(Base):
    """Model for storing the outcome of each health check run against a site"""

    __tablename__ = "health_checks"

    # Primary Key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )

    site_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("websites.site_id"),
        nullable=False
    )

    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    site_stat: Mapped[SiteStatus] = mapped_column(SAEnum(SiteStatus, name="site_status"), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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
        return f"<HealthCheck(id={self.id}, site_id={self.site_id}, site_stat={self.site_stat})>"
