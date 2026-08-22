from pathlib import Path
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def read_secret(secret_name: str) -> str:
    """Read docker secret and return it's value"""
    secret_path = Path(f"/run/secrets/{secret_name}")

    if secret_path.exists():
        return secret_path.read_text().strip()

    raise ValueError(f"Docker secret not found: {secret_name}")


class Settings(BaseSettings):
    """Application settings throughout lifespan via env vars"""

    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets"
    )

    # App
    PROJECT_NAME: str = "TinyPulse"
    DEBUG: bool = False
    PORT: int = 4567

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Database

    DB_HOST: str
    DB_USER: str
    DB_PORT: str
    DB_NAME: str
    DB_PASS: str = Field(alias="db-password")

    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    CORS_ORIGINS: str | list[str] = Field(default="http://localhost:4000")

    
    @model_validator(mode="before")
    @classmethod
    def parse_settings(cls, values):
        """Parse CORS_ORIGINS from string to list"""
        if "CORS_ORIGINS" in values:
            cors = values["CORS_ORIGINS"]
            if isinstance(cors, str):
                values["CORS_ORIGINS"] = [origin.strip() for origin in cors.split(",") if origin.strip()]
        return values

settings = Settings()