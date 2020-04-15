from __future__ import annotations

import os
import typing

import edgedb
from attr import attrs


@attrs(slots=True, frozen=True, auto_attribs=True)
class EdgeDBConnection:
    dsn: typing.Optional[str] = None
    host: typing.Optional[str] = None
    port: int = 5656
    admin: typing.Optional[bool] = False
    user: typing.Optional[str] = None
    password: typing.Optional[str] = None
    database: typing.Optional[str] = None
    timeout: int = 60

    def __call__(
        self, action: str = "async"
    ) -> typing.Union[
        edgedb.BlockingIOConnection,
        typing.Coroutine[typing.Any, typing.Any, edgedb.AsyncIOConnection],
    ]:
        if action not in ("sync", "async"):  # TODO: Refactor to Enum
            raise TypeError(
                f"'Action' must be one of 'sync' or 'async'. You provided '{action}'"
            )
        if action == "async":
            return self.connect_async()
        return self.connect_sync()

    def connect_sync(
        self, connection: typing.Optional[EdgeDBConnection] = None,
    ) -> edgedb.BlockingIOConnection:
        return edgedb.connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=bool(self.admin),
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        )

    async def connect_async(
        self, connection: typing.Optional[EdgeDBConnection] = None,
    ) -> edgedb.AsyncIOConnection:
        return await edgedb.async_connect(
            dsn=self.dsn,
            host=self.host,
            port=self.port,
            admin=bool(self.admin),
            user=self.user,
            password=self.password,
            database=self.database,
            timeout=self.timeout,
        )
