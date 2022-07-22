from ..ConnectionInfo import ConnectionInfo
import asyncpg
from contextlib import asynccontextmanager
from .abstract import AbstractAdapter
from typing import Any

__all__ = [
    "PostgreSQLAdapter"
]

class PostgresSQLAdapter(AbstractAdapter):

    identifier = "asyncpg" # The identifier for this adapter

    def __init__(self, connection : ConnectionInfo) -> None:

        self._connection_info = connection

    async def establish_connection(self) -> asyncpg.Pool:
        """Connects to the server and returns a connection pool

        :return: Connection pool
        :rtype: asyncpg.Pool
        """

        pool = await asyncpg.create_pool( **self._connection_info.as_dict )

        return pool

    @asynccontextmanager
    async def acquire(self) -> asyncpg.Connection:
        with self.pool.acquire() as t:
            yield t
