# Pydantic models are used for API Request validation & Response serialization
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import SiteStatus


class HealthCheckResponse(BaseModel):
    """Result of a single on-demand health probe against a site"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    site_id: UUID
    status_code: int | None
    message: str | None
    site_stat: SiteStatus
    date_created: datetime
