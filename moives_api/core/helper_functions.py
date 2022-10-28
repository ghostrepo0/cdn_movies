import orjson


def orjson_dumps(obj, *, default):
    return orjson.dumps(
        obj,
        default=default,
    ).decode()
