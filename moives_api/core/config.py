import logging
import os
from logging import config as logging_config
from pathlib import Path

import backoff
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class ElasticConnectionConfig(BaseSettings):
    host: str = Field(..., env="ELASTICSEARCH_HOST")
    port: int = Field(..., env="ELASTICSEARCH_PORT")


class RedisConnectionConfig(BaseSettings):
    host: str = Field(..., env="REDIS_HOST")
    port: int = Field(..., env="REDIS_PORT")


class ServiceConnectionConfig(BaseSettings):
    host: str = Field(..., env="FASTAPI_SERVICE_HOST")
    port: int = Field(..., env="FASTAPI_SERVICE_PORT")
    secret_key: str = Field(..., env="SECRET_KEY")
    jwt_hashing_algorithm: str = Field(..., env="JWT_HASHING_ALGORITHM")


ELASTIC_CONF = ElasticConnectionConfig()
REDIS_CONF = RedisConnectionConfig()
SERVICE_CONF = ServiceConnectionConfig()

PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

BASE_DIR = Path(__file__).parent.parent

CACHE_EXPIRE_IN_SECONDS = 60 * int(os.getenv("CACHE_EXPIRE_IN_MINUTES", 5))  # 5 минут

logger = logging.getLogger(__name__)

BACKOFF_CONFIG = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "logger": logger,
    "max_tries": 10,
}
