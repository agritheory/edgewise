import pytest
import edgedb

from edgewise import EdgeDBConnection


@pytest.mark.usefixtures("connection_object")
def test_connection_object(connection_object):
    assert connection_object.host == "localhost"
    assert connection_object.port == 5656
    assert connection_object.admin is False
    assert connection_object.timeout == 60
    assert connection_object.user == "edgedb"
    assert connection_object.password == "edgedb"
    assert connection_object.database == "edgedb"


@pytest.mark.usefixtures("connection_object")
def test_edgedb_sync_connection(connection_object):
    sync_connection = connection_object("sync")
    assert isinstance(sync_connection, edgedb.BlockingIOConnection)
    # close and assert is closed


@pytest.mark.usefixtures("connection_object")
@pytest.mark.asyncio
async def test_edgedb_async_connections(connection_object):
    async_connection = await connection_object("async")
    assert isinstance(async_connection, edgedb.AsyncIOConnection)
    # close and assert is closed
