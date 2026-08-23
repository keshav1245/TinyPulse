import logging
from uuid import UUID

import httpx
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ConflictError, NotFoundError
from app.models.downtime import Downtime
from app.models.enums import SiteStatus
from app.models.health_check import HealthCheck
from app.models.site_registry import Website
from app.repositories.downtime_repository import DowntimeRepository
from app.repositories.health_check_repository import HealthCheckRepository
from app.repositories.website_repository import WebsiteRepository
from app.schemas.downtime import DowntimeResponse
from app.schemas.health_check import HealthCheckResponse
from app.schemas.sites import SiteResponse, SiteCreate

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 10.0


class WebsiteService:

    def __init__(
            self,
            website_repo: WebsiteRepository,
            health_check_repo: HealthCheckRepository,
            downtime_repo: DowntimeRepository
    ):
        logger.info("[SERVICE] Initialising Website Service")
        self.repo = website_repo
        self.health_check_repo = health_check_repo
        self.downtime_repo = downtime_repo
        logger.info("[SERVICE] WebsiteService Initialised !")


    async def create_site(
        self,
        payload: SiteCreate
    ) -> SiteResponse:
        logger.info("[SERVICE] Registering a Website")

        url = payload.url
        port_str = f":{url.port}" if url.port else ""
        site_url: str = f"{url.scheme}://{url.host}{port_str}"

        website = Website(
            url=site_url,
            name=payload.name,
            check_interval=payload.interval,
            is_active=payload.is_active
        )

        try:
            res = await self.repo.create(website)
        except IntegrityError as e:
            raise ConflictError(f"Site '{site_url}' is already registered") from e

        return self._to_response(res)

    async def get_site(self, site_id: UUID) -> SiteResponse:
        logger.info("[SERVICE] Fetching a website by site_id")

        site = await self.repo.get_by_site_id(site_id)
        if site is None:
            raise NotFoundError(f"Site '{site_id}' not found")

        latest_check = await self.health_check_repo.get_latest_for_site(site_id)
        return self._to_response(site, latest_check)

    async def get_all_sites(self) -> list[SiteResponse]:
        logger.info("[SERVICE] Fetching all websites")

        sites = await self.repo.get_all()
        latest_checks = await self.health_check_repo.get_latest_by_site_ids(
            [site.site_id for site in sites]
        )

        return [self._to_response(site, latest_checks.get(site.site_id)) for site in sites]

    async def get_health_checks(self, site_id: UUID, limit: int = 500) -> list[HealthCheckResponse]:
        logger.info("[SERVICE] Fetching health check history for a website")

        site = await self.repo.get_by_site_id(site_id)
        if site is None:
            raise NotFoundError(f"Site '{site_id}' not found")

        checks = await self.health_check_repo.get_all_for_site(site_id, limit=limit)
        return [HealthCheckResponse.model_validate(check) for check in checks]

    async def get_downtimes(self, site_id: UUID, limit: int = 500) -> list[DowntimeResponse]:
        logger.info("[SERVICE] Fetching downtime history for a website")

        site = await self.repo.get_by_site_id(site_id)
        if site is None:
            raise NotFoundError(f"Site '{site_id}' not found")

        downtimes = await self.downtime_repo.get_all_for_site(site_id, limit=limit)
        return [self._to_downtime_response(downtime) for downtime in downtimes]

    async def check_health(self, site_id: UUID) -> HealthCheckResponse:
        logger.info("[SERVICE] Running on-demand health check")

        site = await self.repo.get_by_site_id(site_id)
        if site is None:
            raise NotFoundError(f"Site '{site_id}' not found")

        status_code, message, site_stat = await self._probe(site.url)

        health_check = await self.health_check_repo.create(
            HealthCheck(
                site_id=site.site_id,
                status_code=status_code,
                message=message,
                site_stat=site_stat
            )
        )

        await self._sync_downtime(site.site_id, health_check, site_stat)

        return HealthCheckResponse.model_validate(health_check)

    async def _probe(self, url: str) -> tuple[int | None, str | None, SiteStatus]:
        """Make a live HTTP request to a site and classify the outcome"""

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = await client.get(url)
        except httpx.RequestError as e:
            logger.warning(f"[HEALTH_CHECK] Request to {url} failed: {e}")
            return None, str(e), SiteStatus.DOWN

        if response.status_code < 400:
            return response.status_code, None, SiteStatus.UP

        return response.status_code, f"Received HTTP {response.status_code}", SiteStatus.DOWN

    async def _sync_downtime(self, site_id: UUID, health_check: HealthCheck, site_stat: SiteStatus) -> None:
        """Open a new downtime episode on first failure, close it on recovery"""

        open_downtime = await self.downtime_repo.get_open_for_site(site_id)

        if site_stat is SiteStatus.DOWN and open_downtime is None:
            await self.downtime_repo.create(
                Downtime(health_check_id=health_check.id, start_time=health_check.date_created)
            )
        elif site_stat is SiteStatus.UP and open_downtime is not None:
            open_downtime.end_time = health_check.date_created
            await self.downtime_repo.update(open_downtime)

    def _to_response(self, site: Website, latest_check: HealthCheck | None = None) -> SiteResponse:
        return SiteResponse(
            url=site.url,
            name=site.name,
            interval=site.check_interval,
            is_active=site.is_active,
            site_id=site.site_id,
            latest_health_check=HealthCheckResponse.model_validate(latest_check) if latest_check else None
        )

    def _to_downtime_response(self, downtime: Downtime) -> DowntimeResponse:
        duration_seconds = None
        if downtime.end_time is not None:
            duration_seconds = (downtime.end_time - downtime.start_time).total_seconds()

        return DowntimeResponse(
            id=downtime.id,
            health_check_id=downtime.health_check_id,
            start_time=downtime.start_time,
            end_time=downtime.end_time,
            duration_seconds=duration_seconds
        )
