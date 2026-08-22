import logging

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base

logger = logging.getLogger(__file__)


class BaseRepository[ModelType: Base]:
    """Base repository for common CRUD ops definitions"""

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    def _has_field(self, field: str) -> bool:
        return hasattr(self.model, field)

    async def create(self, obj_in: ModelType) -> ModelType:
        """Create a new record for this model type"""
        self.db.add(obj_in)
        await self.db.flush()
        await self.db.refresh(obj_in)
        return obj_in

    async def soft_delete(self, db_obj: ModelType) -> ModelType:
        if not self._has_field("is_active"):
            raise NotImplementedError(f"Soft delete requires '{self.model.__name__}' to have an 'is_active' column")

        if not db_obj.is_active:
            raise ValueError(f"{self.model.__name__} is already inactive")

        db_obj.is_active = False
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj