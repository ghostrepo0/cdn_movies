from typing import Optional

import orjson
from jwt import decode

from src.core.config import SERVICE_CONF


def orjson_dumps(obj, *, default):
    return orjson.dumps(
        obj,
        default=default,
    ).decode()


def decode_cookie(token: Optional[str]) -> dict[str, str]:

    if token is None:
        return {}

    return decode(
        jwt=token,
        key=SERVICE_CONF.secret_key,
        do_verify=True,
        do_time_check=True,
        algorithms=SERVICE_CONF.algorithm,
    )
