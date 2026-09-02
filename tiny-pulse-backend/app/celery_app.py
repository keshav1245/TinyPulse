from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tiny_pulse",
    broker=settings.REDIS_URL,
    include=["app.tasks.health_check_task", "app.tasks.notification_task"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    broker_connection_retry_on_startup=True,
    beat_scheduler="redbeat.RedBeatScheduler",
    redbeat_redis_url=settings.REDBEAT_REDIS_URL,
    redbeat_key_prefix="tinypulse:redbeat:",
)