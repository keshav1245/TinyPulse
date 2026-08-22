import logging

from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.website_service import WebsiteService
from app.schemas.sites import SiteCreate, SiteCreateResponse
from fastapi import APIRouter, status, Depends, HTTPException
from app.repositories.website_repository import WebsiteRepository

router = APIRouter()
logger = logging.getLogger(__file__)

async def get_website_service(db: AsyncSession = Depends(get_db)) -> WebsiteService:
    logger.info("[DEPENDENCY] Creating website service instance")
    web_repo = WebsiteRepository(db)
    web_service = WebsiteService(website_repo=web_repo)
    logger.info("[DEPENDENCY] Website Service created successfully")
    return web_service



@router.post(
    "/",
    response_model=SiteCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_site(
    data: SiteCreate,
    service: WebsiteService = Depends(get_website_service)
):
    logger.info("[ENDPOINT] Creating a website")

    try:
        return await service.create_site(data)
    except Exception as e:
        logger.error(f"[ENDPOINT] Failed to create site: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create website: {e!s}"
        )