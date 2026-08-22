# Pydantic models are used for API Request validation & Response serialization
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from uuid import UUID

class SiteBase(BaseModel):
    """Base fields for a site"""
    url: HttpUrl = Field(..., description="Website url entered by user")
    name: str = Field(..., max_length=100)
    interval: int = Field(default=120)

class SiteCreate(SiteBase):
    """Add a site to db"""
    is_active: bool = Field(default=True)

class SiteCreateResponse(SiteCreate):
    site_id: UUID
    
class SiteGETResponse(BaseModel):

    """Returning single site from db"""
    model_config = ConfigDict(from_attributes=True)

    site_id: UUID
    url: HttpUrl
    name: str
