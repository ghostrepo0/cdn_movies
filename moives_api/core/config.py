import logging
import os
from logging import config as logging_config
from pathlib import Path

import backoff
from core.logger import LOGGING
from pydantic import BaseSettings, Field

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

    film_bucket_name: str = Field(..., env="FILM_BUCKET_NAME")


class PostgresConnectionConfig(BaseSettings):
    dbname: str = Field(..., env="POSTGRES_DB")
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    host: str = Field(..., env="POSTGRES_HOST")
    port: int = Field(..., env="POSTGRES_PORT")


class MinioNode1ConnectionConfig(BaseSettings):
    host: str = Field(..., env="MINIO_NODE_1_HOST")
    port: int = Field(..., env="MINIO_NODE_1_PORT")
    access_key: str = Field(..., env="MINIO_NODE_1_ACCESS_KEY")
    secret_key: str = Field(..., env="MINIO_NODE_1_SECRET_KEY")


class MinioNode2ConnectionConfig(BaseSettings):
    host: str = Field(..., env="MINIO_NODE_2_HOST")
    port: int = Field(..., env="MINIO_NODE_2_PORT")
    access_key: str = Field(..., env="MINIO_NODE_2_ACCESS_KEY")
    secret_key: str = Field(..., env="MINIO_NODE_2_SECRET_KEY")


ELASTIC_CONF = ElasticConnectionConfig()
REDIS_CONF = RedisConnectionConfig()
SERVICE_CONF = ServiceConnectionConfig()
POSTGRES_CONF = PostgresConnectionConfig()

MINIO_NODE1 = MinioNode1ConnectionConfig()
MINIO_NODE2 = MinioNode2ConnectionConfig()

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
