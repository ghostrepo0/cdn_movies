from datetime import timedelta
from functools import lru_cache
from random import choice
from typing import Optional

from asyncpg import Connection
from core.config import SERVICE_CONF
from db.minio import get_minio_client_1, get_minio_client_2
from db.postgres import get_pg_conn
from fastapi import Depends
from minio import Minio


class DownloadFilm:
    def __init__(
        self,
        minio_client_1: Minio,
        minio_client_2: Minio,
        postgres_conn: Connection,
    ):
        self.minio_client_1: Minio = minio_client_1
        self.minio_client_2: Minio = minio_client_2

        self.postgres_conn: Connection = postgres_conn

    @property
    def minio_client(self) -> Minio:
        return choice((self.minio_client_1, self.minio_client_2))

    async def get_download_url(
        self,
        film_id: str,
        ip_address: str,
    ) -> Optional[str]:

        film_file_name: Optional[str] = await self._get_film_file_name(film_id)

        if film_file_name is None:
            return None

        return await self._make_download_url(
            film_file_name,
            ip_address,
        )

    async def _get_film_file_name(
        self,
        film_id: str,
        /,
    ) -> Optional[str]:

        values = await self.postgres_conn.fetch(
            f"SELECT file_path FROM content.film_work WHERE id = '{film_id}'"
        )

        if len(values) < 1:
            return None

        return values[0]["file_path"]

    async def _make_download_url(
        self,
        file_name: str,
        ip_address: str,  # noqa
    ) -> Optional[str]:

        minio_client = self.minio_client

        if not minio_client.bucket_exists(SERVICE_CONF.film_bucket_name):
            return None

        if not any(
            file_name == bucket_object.object_name
            for bucket_object in minio_client.list_objects(
                SERVICE_CONF.film_bucket_name
            )
        ):
            return None

        return minio_client.presigned_get_object(
            SERVICE_CONF.film_bucket_name,
            file_name,
            expires=timedelta(minutes=10),
        )


@lru_cache()
def get_file_download_service(
    pg_conn: Connection = Depends(get_pg_conn),
    minio_client_1: Minio = Depends(get_minio_client_1),
    minio_client_2: Minio = Depends(get_minio_client_2),
) -> DownloadFilm:
    return DownloadFilm(
        minio_client_1=minio_client_1,
        minio_client_2=minio_client_2,
        postgres_conn=pg_conn,
    )
