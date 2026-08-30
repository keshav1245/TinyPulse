from celery.signals import worker_process_init
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SYNC_DATABASE_URL,
                       pool_pre_ping=True)

SyncSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

@worker_process_init.connect
def _dispose_engine_in_worker_child(**kwargs) -> None:
    engine.dispose()