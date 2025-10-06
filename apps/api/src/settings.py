from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://app:app@localhost:5432/swampnotes"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_ACCESS_KEY_ID: str = "minio"
    S3_SECRET_ACCESS_KEY: str = "minio12345"
    S3_BUCKET: str = "swampnotes"
    ALLOWED_EMAIL_DOMAINS: list[str] = ["school.edu"]
    AUTH_JWKS_URL: str | None = None  # should link to Auth0/Clerk/NextAuth JWTs
    class Config:
        env_file = ".env"

settings = Settings()