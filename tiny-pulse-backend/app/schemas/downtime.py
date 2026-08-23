# Pydantic models are used for API Request validation & Response serialization
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DowntimeResponse(BaseModel):
    """A single continuous downtime episode for a site"""

    id: UUID
    health_check_id: UUID
    start_time: datetime
    end_time: datetime | None
    duration_seconds: float | None
