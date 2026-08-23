"""Downtime model - tracks a single continuous downtime episode for a site"""

from datetime import datetime
from uuid import uuid4

from app.db.base import Base

from sqlalchemy import func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column


class Downtime(Base):
    """Model for tracking a downtime episode, from the health check that first
    detected it to the one that resolved it"""

    __tablename__ = "downtimes"

    # Primary Key
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=func.gen_random_uuid()
    )

    health_check_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("health_checks.id"),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

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
        return f"<Downtime(id={self.id}, health_check_id={self.health_check_id}, end_time={self.end_time})>"
