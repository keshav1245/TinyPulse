import logging
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.db.sync_session import SyncSessionLocal
from app.models.downtime import Downtime
from app.models.enums import SiteStatus
from app.models.health_check import HealthCheck
from app.models.site_registry import Website

from app.tasks.notification_task import send_downtime_email, send_uptime_email

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10.0

@celery_app.task(name="health_check.run")
def run_health_check(site_id: str) -> None:
    with SyncSessionLocal() as db:
        site = db.execute(
            select(Website).where(Website.site_id == UUID(site_id),
                                  Website.is_active.is_(True))
        ).scalar_one_or_none()

        if site is None:
            logger.info(f"[CELERY] Site {site_id} is inactive or no longer exists, skipping")
            return

        status_code, message, site_stat = _probe(site.url)

        health_check = HealthCheck(
            site_id=site.site_id,
            status_code=status_code,
            message=message,
            site_stat=site_stat
        )

        db.add(health_check)
        db.flush()
        db.refresh(health_check)

        _sync_downtime(db, site, health_check, site_stat)

        db.commit()
        logger.info(f"[CELERY] Checked {site.url} -> {site_stat.value}")



def _probe(url: str) -> tuple[int | None, str | None, SiteStatus]:
    try:
        with httpx.Client(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
            resp = client.get(url)
    except httpx.RequestError as e:
        logger.warning(f"[CELERY] Request to {url} failed: {e}")
        return None, str(e), SiteStatus.DOWN

    if resp.status_code < 400:
        return resp.status_code, None, SiteStatus.UP

    return resp.status_code, f"Received HTTP {resp.status_code}", SiteStatus.DOWN


def _sync_downtime(db: Session, site: Website, health_check: HealthCheck, site_stat: SiteStatus) -> None:
    open_downtime = db.execute(
        select(Downtime)
        .join(HealthCheck, Downtime.health_check_id == HealthCheck.id)
        .where(HealthCheck.site_id == site.site_id, Downtime.end_time.is_(None))
    ).scalar_one_or_none()

    if site_stat is SiteStatus.DOWN and open_downtime is None:
        db.add(Downtime(health_check_id=health_check.id, start_time=health_check.date_created))
        send_downtime_email.delay(site.name or site.url, site.url)
    elif site_stat is SiteStatus.UP and open_downtime is not None:
        open_downtime.end_time = health_check.date_created
        duration_seconds = (open_downtime.end_time - open_downtime.start_time).total_seconds()
        send_uptime_email.delay(site.name or site.url, site.url, duration_seconds)

        
