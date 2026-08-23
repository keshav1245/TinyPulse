# Pydantic models are used for API Request validation & Response serialization
from datetime import date as date_
from uuid import UUID

from pydantic import BaseModel


class DailyStat(BaseModel):
    """Aggregated health-check & downtime numbers for a single calendar day"""

    date: date_
    total_checks: int
    up_checks: int
    down_checks: int
    uptime_percentage: float | None
    downtime_seconds: float
    incident_count: int


class SiteDailyStatsResponse(BaseModel):
    """Daily aggregate stats for a site over a rolling window, one entry per day"""

    site_id: UUID
    days: int
    daily_stats: list[DailyStat]
