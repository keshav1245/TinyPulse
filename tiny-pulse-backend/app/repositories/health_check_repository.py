import logging
from collections.abc import Sequence
from datetime import datetime
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.enums import SiteStatus
from app.models.health_check import HealthCheck
from app.repositories.base import BaseRepository

logger = logging.getLogger(__file__)

class HealthCheckRepository(BaseRepository[HealthCheck]):

    def __init__(self, db: AsyncSession):
        super().__init__(HealthCheck, db)

    async def get_latest_for_site(self, site_id: UUID, is_active: bool = True) -> HealthCheck | None:
        """Fetch the most recent health check recorded for a site"""

        logger.info("[HEALTH_CHECK_REPO] Fetching latest health check for site")
        query = select(HealthCheck).where(HealthCheck.site_id == site_id)

        if is_active:
            query = query.where(HealthCheck.is_active.is_(True))

        query = query.order_by(HealthCheck.date_created.desc()).limit(1)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_latest_by_site_ids(
        self,
        site_ids: Sequence[UUID],
        is_active: bool = True
    ) -> dict[UUID, HealthCheck]:
        """Fetch the most recent health check for each of the given sites in one query"""

        if not site_ids:
            return {}

        logger.info("[HEALTH_CHECK_REPO] Fetching latest health checks for multiple sites")
        query = select(HealthCheck).where(HealthCheck.site_id.in_(site_ids))

        if is_active:
            query = query.where(HealthCheck.is_active.is_(True))

        # DISTINCT ON (site_id) + matching leading ORDER BY - postgres' "latest row per group" idiom
        query = query.distinct(HealthCheck.site_id).order_by(
            HealthCheck.site_id, HealthCheck.date_created.desc()
        )

        result = await self.db.execute(query)
        return {hc.site_id: hc for hc in result.scalars().all()}

    async def get_all_for_site(
        self,
        site_id: UUID,
        limit: int = 500,
        is_active: bool = True
    ) -> Sequence[HealthCheck]:
        """Fetch the most recent `limit` health checks for a site, oldest first"""

        logger.info("[HEALTH_CHECK_REPO] Fetching health check history for site")
        query = select(HealthCheck).where(HealthCheck.site_id == site_id)

        if is_active:
            query = query.where(HealthCheck.is_active.is_(True))

        query = query.order_by(HealthCheck.date_created.desc()).limit(limit)

        result = await self.db.execute(query)
        return list(reversed(result.scalars().all()))

    async def get_daily_counts(
        self,
        site_id: UUID,
        since: datetime,
        is_active: bool = True
    ) -> Sequence[Row]:
        """Count checks per calendar day since a given timestamp, split by UP/DOWN"""

        logger.info("[HEALTH_CHECK_REPO] Fetching daily check counts for site")
        day_col = func.date_trunc("day", HealthCheck.date_created).label("day")

        query = select(
            day_col,
            func.count().label("total"),
            func.count(case((HealthCheck.site_stat == SiteStatus.UP, 1))).label("up_count"),
            func.count(case((HealthCheck.site_stat == SiteStatus.DOWN, 1))).label("down_count"),
        ).where(HealthCheck.site_id == site_id, HealthCheck.date_created >= since)

        if is_active:
            query = query.where(HealthCheck.is_active.is_(True))

        query = query.group_by(day_col).order_by(day_col)

        result = await self.db.execute(query)
        return result.all()
