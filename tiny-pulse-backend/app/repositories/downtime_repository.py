import logging
from collections.abc import Sequence
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.downtime import Downtime
from app.models.health_check import HealthCheck
from app.repositories.base import BaseRepository

logger = logging.getLogger(__file__)

class DowntimeRepository(BaseRepository[Downtime]):

    def __init__(self, db: AsyncSession):
        super().__init__(Downtime, db)

    async def get_open_for_site(self, site_id: UUID) -> Downtime | None:
        """Fetch the currently ongoing downtime episode for a site, if any"""

        logger.info("[DOWNTIME_REPO] Fetching open downtime for site")
        query = (
            select(Downtime)
            .join(HealthCheck, Downtime.health_check_id == HealthCheck.id)
            .where(HealthCheck.site_id == site_id, Downtime.end_time.is_(None))
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_for_site(
        self,
        site_id: UUID,
        limit: int = 500,
        is_active: bool = True
    ) -> Sequence[Downtime]:
        """Fetch the most recent `limit` downtime episodes for a site, oldest first"""

        logger.info("[DOWNTIME_REPO] Fetching downtime history for site")
        query = (
            select(Downtime)
            .join(HealthCheck, Downtime.health_check_id == HealthCheck.id)
            .where(HealthCheck.site_id == site_id)
        )

        if is_active:
            query = query.where(Downtime.is_active.is_(True))

        query = query.order_by(Downtime.start_time.desc()).limit(limit)

        result = await self.db.execute(query)
        return list(reversed(result.scalars().all()))

    async def get_since_for_site(
        self,
        site_id: UUID,
        since: datetime,
        is_active: bool = True
    ) -> Sequence[Downtime]:
        """Fetch downtime episodes that started on/after a given timestamp"""

        logger.info("[DOWNTIME_REPO] Fetching downtimes since a timestamp for site")
        query = (
            select(Downtime)
            .join(HealthCheck, Downtime.health_check_id == HealthCheck.id)
            .where(HealthCheck.site_id == site_id, Downtime.start_time >= since)
        )

        if is_active:
            query = query.where(Downtime.is_active.is_(True))

        query = query.order_by(Downtime.start_time.asc())

        result = await self.db.execute(query)
        return result.scalars().all()
