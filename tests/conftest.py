import asyncio
import tracemalloc

import pytest

import edgewise
from tests.create_data import user_schema, create_company, create_user, create_rbac_role

tracemalloc.start()

def get_connection_object():
    return edgewise.EdgeDBConnection(
        dsn=None,
        host="localhost",
        port=5656,
        admin=False,
        user="edgedb",
        password="edgedb",
        database="edgedb",
        timeout=60,
    )


def pytest_configure(config):
    connection_object = get_connection_object()
    conn = connection_object("sync")
    with conn.transaction():
        conn.execute(user_schema)
        print("Imported Schema")
    edgewise.class_registry = edgewise.ClassRegistry(connection_object)
    asyncio.run(create_company())
    asyncio.run(create_rbac_role())
    asyncio.run(create_user())
    print("Registered Classes:")
    [
        print("{}: {}".format(key, value))
        for key, value in edgewise.class_registry.registry.items()
    ]



@pytest.fixture(scope="module")
def connection_object():
    return get_connection_object()
