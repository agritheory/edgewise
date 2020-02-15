import edgedb
import dotenv
import os
import typing


def load_connection_from_environment() -> edgedb.con_utils.ConnectionParameters:
    dotenv.load_dotenv()
    return edgedb.con_utils.ConnectionParameters(
        user=os.getenv("EDGEDB_USER", default="edgedb"),
        password=os.getenv("EDGEDB_PASSWORD"),
        database=os.getenv("EDGEDB_DATABASE", default="example"),
        connect_timeout=os.getenv("EDGEDB_TIMEOUT", default="60"),
        server_settings={"host": os.getenv("EDGEDB_HOST", default="localhost")},
    )


def connect(
    connection: typing.Optional[edgedb.con_utils.ConnectionParameters] = None,
    sync_or_async: str = "async",
) -> typing.Union[edgedb.BlockingIOConnection, edgedb.AsyncIOConnection]:
    if sync_or_async == "async":
        return connect_async(**connection)
    return connect_sync(**connection)


def connect_sync(
    connection: typing.Optional[edgedb.con_utils.ConnectionParameters] = None,
) -> edgedb.BlockingIOConnection:
    if not connection:
        connection = load_connection_from_environment()
    return edgedb.connect(connection)


async def connect_async(
    connection: typing.Optional[edgedb.con_utils.ConnectionParameters] = None,
) -> edgedb.AsyncIOConnection:
    if not connection:
        connection = load_connection_from_environment()
    return edgedb.connect_async(connection)
