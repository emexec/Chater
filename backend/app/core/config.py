import os
import ssl

from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Base config of project"""
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_HOST: str

    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(), '..'))

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env"
    )


settings = Settings()

redis_url = f"rediss://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)
celery_app.conf.update(broker_use_ssl=ssl_options, redis_backend_use_ssl=ssl_options)
