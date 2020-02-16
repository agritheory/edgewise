from __future__ import annotations

import os
import typing

import dotenv
import edgedb
from attr import attrs


@attrs(slots=True, frozen=True, auto_attribs=True)
class EdgeDBConnection:
    dsn: typing.Optional[str] = os.getenv("EDGEDB_DSN", default=None)
    host: typing.Optional[str] = os.getenv("EDGEDB_HOST", default="localhost")
    port: int = os.getenv("EDGEDB_PORT", default=5656)
    admin: typing.Optional[bool] = os.getenv("EDGEDB_ADMIN", default=False)
    user: typing.Optional[str] = os.getenv("EDGEDB_USER")
    password: typing.Optional[str] = os.getenv("EDGEDB_PASSWORD")
    database: typing.Optional[str] = os.getenv("EDGEDB_DATABASE")
    timeout: int = os.getenv("EDGEDB_TIMEOUT", default=60)

    def __call__(
        self, action: str = "async"
    ) -> typing.Union[edgedb.BlockingIOConnection, edgedb.AsyncIOConnection]:
        if action not in ("sync", "async"):
            raise TypeError(
                f"'Action' must be one of 'sync' or 'async'. You provided '{action}'"
            )
        if action == "async":
            return self.connect_async()
        return self.connect_sync()

    def connect_sync(
        self,
        connection: typing.Optional[EdgeDBConnection] = None,
    ) -> edgedb.BlockingIOConnection:
        return edgedb.connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=self.admin,
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        )

    async def connect_async(
        self,
        connection: typing.Optional[EdgeDBConnection] = None,
    ) -> edgedb.AsyncIOConnection:
        return await edgedb.async_connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=self.admin,
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        )

    # not sure if this is needed
    def close(self) -> typing.NoReturn:
        edgedb.connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=self.admin,
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        ).close()

    # not sure if this is needed
    def aclose(self) -> typing.NoReturn:
        conn = await edgedb.connect_async(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=self.admin,
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        )
        await conn.aclose()
