import asyncio
import typing
from importlib import import_module

import pytest
from attr import attrs

from edgewise import EdgeDBConnection, ClassRegistry, init_class_registry, class_registry
from tests.create_data import user_schema, create_company, create_user, create_rbac_role


def get_connection_object() -> EdgeDBConnection:
    return EdgeDBConnection(
        dsn=None,
        host="localhost",
        port=5656,
        admin=False,
        user="edgedb",
        password="edgedb",
        database="edgedb",
        timeout=60,
    )


def pytest_configure(config) -> typing.NoReturn:
    connection_object = get_connection_object()
    conn = connection_object("sync")
    with conn.transaction():
        conn.execute(user_schema)
        print("Imported Schema")
    conn.close()
    global class_registry
    class_registry = init_class_registry(connection_object)
    asyncio.run(create_company())
    asyncio.run(create_rbac_role())
    asyncio.run(create_user())
    print("Registered Classes:")
    [
        print("{}: {}".format(key, value))
        for key, value in class_registry.registry.items()
    ]


@pytest.fixture(scope="module")
def connection_object() -> EdgeDBConnection:
    return get_connection_object()
