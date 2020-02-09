import edgedb
import dotenv
import os
import typing


def connect_sync(connection: typing.Optional[edgedb.BlockingIOConnection] = None) -> edgedb.BlockingIOConnection:
    dotenv.load_dotenv()
    return edgedb.connect(
        host=os.getenv("EDGEDB_HOST", default="localhost"),
        user=os.getenv("EDGEDB_USER", default="edgedb"),
        password=os.getenv("EDGEDB_PASSWORD"),
        database=os.getenv("EDGEDB_DATABASE", default="example"),
    )


def connect_async():
    dotenv.load_dotenv()
    return edgedb.async_connect(
        host=os.getenv("EDGEDB_HOST", default="localhost"),
        user=os.getenv("EDGEDB_USER", default="edgedb"),
        password=os.getenv("EDGEDB_PASSWORD"),
        database=os.getenv("EDGEDB_DATABASE", default="example"),
    )

def load_edgeql_file(path) -> str:
    pass
