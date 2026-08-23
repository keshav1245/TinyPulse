import logging
from uuid import UUID

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.website_service import WebsiteService
from app.schemas.sites import SiteCreate, SiteResponse
from app.schemas.health_check import HealthCheckResponse
from fastapi import APIRouter, status, Depends
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
