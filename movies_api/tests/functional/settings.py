import os

from pydantic import BaseSettings, Field

run_tests_locally = os.getenv('LOCAL_TESTS', None)
if run_tests_locally:
    class TestSettings(BaseSettings):
        es_host: str = 'http://127.0.0.1:9200'
        service_url: str = 'http://0.0.0.0:80'
        api_url: str = '/api/v1/'
        redis_host: str = '127.0.0.1'
        redis_port: int = 6379
else:
    class TestSettings(BaseSettings):
        es_host: str = Field(env='ELASTIC_HOST')
        service_url: str = Field(env='SERVICE_URL')
        api_url: str = Field(env='API_URL')
        redis_host: str = Field(env='REDIS_HOST')
        redis_port: int = Field(env='REDIS_PORT')

settings = TestSettings()
