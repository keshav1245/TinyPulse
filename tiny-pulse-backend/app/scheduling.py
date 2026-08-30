from uuid import UUID

from celery.schedules import schedule as celery_schedule
from redbeat import RedBeatSchedulerEntry

from app.celery_app import celery_app

TASK_NAME = "health_check.run"

def _entry_name(site_id: UUID | str) -> str: 
    return f"health_check:{site_id}"

def schedule_site(site_id: UUID | str, interval_seconds: int) -> None:
    entry = RedBeatSchedulerEntry(
        name=_entry_name(site_id),
        task=TASK_NAME,
        schedule=celery_schedule(run_every=interval_seconds),
        args=[str(site_id)],
        app=celery_app
    )
    entry.save()

def unschedule_site(site_id: UUID | str) -> None:
    key = celery_app.conf.redbeat_key_prefix + _entry_name(site_id)
    try: 
        RedBeatSchedulerEntry.from_key(key, app=celery_app).delete()
    except KeyError:
        pass