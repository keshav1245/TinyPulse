import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.health_check import HealthCheck
from app.repositories.base import BaseRepository

logger = logging.getLogger(__file__)

class HealthCheckRepository(BaseRepository[HealthCheck]):

    def __init__(self, db: AsyncSession):
        super().__init__(HealthCheck, db)
