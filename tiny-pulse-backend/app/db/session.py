"""Centralised Database Connection Management"""

import logging
import app.models
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.core.config import settings

logger = logging.getLogger(__name__)
_TABLE_INIT_LOCK_ID  = 42

_db: Database | None = None

class Database:
    """DB Connection manager workflow"""

    def __init__(self, database_url: str):
        self.database_url = database_url

        self.engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=True
        )

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
            future=True
        )

    async def connect(self) -> None:
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info("Connected to database")

        async with self.engine.begin() as conn:
            await conn.execute(text(f"SELECT pg_advisory_xact_lock({_TABLE_INIT_LOCK_ID})"))
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Base tables created")

    async def disconnect(self) -> None:
        if self.engine:
            logger.info("Disconnecting from database")
            await self.engine.dispose()
            logger.info("Database disconnected")


    async def async_session(self) -> AsyncSession:
        return self.session_maker()

def get_database() -> Database:
    if _db is not None:
        return _db

    raise RuntimeError("Database not initialised !")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    database = get_database()

    async with database.session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise