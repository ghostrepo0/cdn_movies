import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = 'movies'
    project_host: str = '0.0.0.0'
    cache_expire_time: int = 60 * 5

    redis_host: str = 'redis'

    redis_port: int = 6379

    elastic_host: str = 'elastic'
    elastic_port: int = 9200


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
