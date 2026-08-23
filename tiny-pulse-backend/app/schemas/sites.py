# Pydantic models are used for API Request validation & Response serialization
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

class SiteBase(BaseModel):
    """Base fields for a site"""
    url: HttpUrl = Field(..., description="Website url entered by user")
    name: str = Field(..., max_length=100)
    interval: int = Field(default=120)

class SiteCreate(SiteBase):
    """Add a site to db"""
    is_active: bool = Field(default=True)

class SiteResponse(SiteCreate):
    """Full representation of a site, returned by create/get endpoints"""
    site_id: UUID
