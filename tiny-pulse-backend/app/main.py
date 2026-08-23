import logging

import app.db.session as sess
from app.db.session import Database
from app.core.config import settings
from app.core.exceptions import AppError
from app.api.v1.router import api_router
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("app").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

APP_VERSION = "0.0.1"

@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup / shutdown"""

    logger.info("🚀 Starting up TinyPulse Service...")
    logger.info("🔗 API Version v1")

    # DB init
    database = Database(settings.DATABASE_URL)
    await database.connect()
    
    sess._db = database

    logger.info("✅ Application Startup Complete !")

    yield

    # Shutdown
    logger.info("👋 Shutting down TinyPulse Service...")
    await database.disconnect()
    logger.info("✅ Shutdown complete")



app = FastAPI(
    title=settings.PROJECT_NAME,
    description="App to trace service downtime in your cluster",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions and ensure CORS headers are included"""
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

    # Add CORS headers to error responses
    origin = request.headers.get("origin")
    if origin and (origin in settings.CORS_ORIGINS or "*" in settings.CORS_ORIGINS):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle domain-level errors and ensure CORS headers are included"""
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

    # Add CORS headers to error responses
    origin = request.headers.get("origin")
    if origin and (origin in settings.CORS_ORIGINS or "*" in settings.CORS_ORIGINS):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions and ensure CORS headers are included"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

    # Add CORS headers to error responses
    origin = request.headers.get("origin")
    if origin and (origin in settings.CORS_ORIGINS or "*" in settings.CORS_ORIGINS):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.PROJECT_NAME,
        "version": APP_VERSION,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy"}