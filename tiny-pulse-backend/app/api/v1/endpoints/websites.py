import logging
from uuid import UUID

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.website_service import WebsiteService
from app.schemas.sites import SiteCreate, SiteResponse
from app.schemas.health_check import HealthCheckResponse
from app.schemas.downtime import DowntimeResponse
from app.schemas.stats import SiteDailyStatsResponse
from fastapi import APIRouter, status, Depends, Query
from app.repositories.website_repository import WebsiteRepository
from app.repositories.health_check_repository import HealthCheckRepository
from app.repositories.downtime_repository import DowntimeRepository

router = APIRouter()
logger = logging.getLogger(__file__)

async def get_website_service(db: AsyncSession = Depends(get_db)) -> WebsiteService:
    logger.info("[DEPENDENCY] Creating website service instance")
    web_repo = WebsiteRepository(db)
    health_check_repo = HealthCheckRepository(db)
    downtime_repo = DowntimeRepository(db)
    web_service = WebsiteService(
        website_repo=web_repo,
        health_check_repo=health_check_repo,
        downtime_repo=downtime_repo
    )
    logger.info("[DEPENDENCY] Website Service created successfully")
    return web_service



@router.post(
    "/",
    response_model=SiteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_site(
    data: SiteCreate,
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Creating a website")
    return await service.create_site(data)


@router.delete(
    "/{site_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_site(
    site_id: UUID,
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Deleting a website")
    await service.delete_site(site_id)


@router.get(
    "/",
    response_model=list[SiteResponse]
)
async def get_all_sites(
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Fetching all websites")
    return await service.get_all_sites()


@router.get(
    "/{site_id}",
    response_model=SiteResponse
)
async def get_site(
    site_id: UUID,
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Fetching a website by site_id")
    return await service.get_site(site_id)


@router.post(
    "/{site_id}/health-checks",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_201_CREATED
)
async def check_health(
    site_id: UUID,
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Running on-demand health check")
    return await service.check_health(site_id)


@router.get(
    "/{site_id}/health-checks",
    response_model=list[HealthCheckResponse]
)
async def get_health_checks(
    site_id: UUID,
    limit: int = Query(default=500, ge=1, le=2000),
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Fetching health check history")
    return await service.get_health_checks(site_id, limit=limit)


@router.get(
    "/{site_id}/downtimes",
    response_model=list[DowntimeResponse]
)
async def get_downtimes(
    site_id: UUID,
    limit: int = Query(default=500, ge=1, le=2000),
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Fetching downtime history")
    return await service.get_downtimes(site_id, limit=limit)


@router.get(
    "/{site_id}/stats",
    response_model=SiteDailyStatsResponse
)
async def get_daily_stats(
    site_id: UUID,
    days: int = Query(default=7, ge=1, le=90),
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Fetching daily stats")
    return await service.get_daily_stats(site_id, days=days)
