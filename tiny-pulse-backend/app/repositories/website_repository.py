import logging
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.site_registry import Website
from app.repositories.base import BaseRepository

logger = logging.getLogger(__file__)

class WebsiteRepository(BaseRepository[Website]):

    def __init__(self, db:AsyncSession):
        super().__init__(Website, db)

    async def get_by_site_id(
        self, 
        site_id: UUID,
        is_active: bool = True
    ) -> Website | None:

        logger.info("[WWEBSITE_REPO] Fetching site data via site_id")
        query = select(Website).where(Website.site_id == site_id)

        if is_active:
            query = query.where(Website.is_active.is_(True))

        result = await self.db.execute(query)
        logger.debug("Data fetching query executed successfully, returning data or none")
        return result.scalar_one_or_none()


        