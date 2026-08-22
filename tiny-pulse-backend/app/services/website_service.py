import logging
from app.models.site_registry import Website
from app.schemas.sites import SiteCreateResponse, SiteCreate
from app.repositories.website_repository import WebsiteRepository

logger = logging.getLogger(__name__)


class WebsiteService:

    def __init__(
            self,
            website_repo: WebsiteRepository
    ):
        logger.info("[SERVICE] Initialising Website Service")
        self.repo = website_repo
        logger.info("[SERVICE] WebsiteService Initialised !")


    async def create_site(
        self,
        payload: SiteCreate
    ) -> SiteCreateResponse:
        logger.info("[SERVICE] Registering a Website")

        url = payload.url
        port_str = f":{url.port}" if url.port else ""
        site_url: str = f"{url.scheme}://{url.host}{port_str}"

        payload = Website(
            url=site_url,
            name=payload.name,
            check_interval=payload.interval,
            is_active=payload.is_active
        )

        res = await self.repo.create(payload)

        return SiteCreateResponse(
            url=res.url,
            name=res.name,
            interval=res.check_interval,
            is_active=res.is_active,
            site_id=res.site_id
        )
