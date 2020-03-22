import pytest
import edgedb

from edgewise import EdgeDBConnection


def get_connection_object():
    return EdgeDBConnection(
        dsn=None,
        host="localhost",
        port=5656,
        admin=False,
        user="edgedb",
        password="edgedb",
        database="edgedb",
        timeout=60
    )


def test_connection_object():
    connection_object = get_connection_object()
    assert connection_object.host == 'localhost'
    assert connection_object.port == 5656
    assert connection_object.admin is False
    assert connection_object.timeout == 60
    assert connection_object.user == 'edgedb'
    assert connection_object.password == 'edgedb'
    assert connection_object.database == 'edgedb'


def test_edgedb_sync_connection():
    connection_object = get_connection_object()
    sync_connection = connection_object('sync')
    assert isinstance(sync_connection, edgedb.BlockingIOConnection)


@pytest.mark.asyncio
async def test_edgedb_async_connections():
    connection_object = get_connection_object()
    async_connection = await connection_object('async')
    assert isinstance(async_connection, coroutine)
