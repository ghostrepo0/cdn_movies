from typing import Optional

from asyncpg import Connection

pg_conn: Optional[Connection] = None


def get_pg_conn() -> Connection:
    return pg_conn
