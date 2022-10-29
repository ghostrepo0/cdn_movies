from typing import Optional

from minio import Minio

minio_client_1: Optional[Minio] = None
minio_client_2: Optional[Minio] = None


async def get_minio_client_1() -> Minio:
    return minio_client_1


async def get_minio_client_2() -> Minio:
    return minio_client_2
