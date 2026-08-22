"""API v1 Router Centrepoint"""
from fastapi import APIRouter
from app.api.v1.endpoints import websites

api_router = APIRouter()


api_router.include_router(
    websites.router,
    prefix="/sites",
    tags=["websites"]
)