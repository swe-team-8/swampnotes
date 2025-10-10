from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=False
    )

    # DB: default to the working local credentials
    DATABASE_URL: str = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/swampnotes"

    # CORS: allow Next.js dev origins by default; can override later in .env as JSON or CSV
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # S3 / MinIO
    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY_ID: str = "minio"
    S3_SECRET_ACCESS_KEY: str = "minio12345"
    S3_BUCKET: str = "swampnotes"

    # Auth-related
    ALLOWED_EMAIL_DOMAINS: list[str] = ["ufl.edu"]
    AUTH_ISSUER: str | None = None  # ex: https://<subdomain>.clerk.accounts.dev
    AUTH_AUDIENCE: str | None = None  # ex: fastapi
    AUTH_JWKS_URL: str | None = None  # optional explicit JWKS URL

    @field_validator("CORS_ORIGINS", "ALLOWED_EMAIL_DOMAINS", mode="before")
    @classmethod
    def _coerce_list(cls, v: Any):
        """
        Accept a JSON array (e.g., '["http://localhost:3000"]') or
        a comma-separated string (e.g., 'http://localhost:3000,http://127.0.0.1:3000') and return list[str].
        """
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                import json

                return json.loads(s)
            return [item.strip() for item in s.split(",") if item.strip()]
        return v


settings = Settings()
