import logging
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
