from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Pipeline Orchestrator"
    APP_ENV: str = "development"
    SECRET_KEY: str = "changeme"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
