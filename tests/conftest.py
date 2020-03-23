import pytest

import edgewise


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
    edgewise.class_registry = edgewise.ClassRegistry(connection_object)
    print("Registered Classes:")
    [
        print("{}: {}".format(key, value))
        for key, value in edgewise.class_registry.registry.items()
    ]


@pytest.fixture(scope="module")
def connection_object():
    return get_connection_object()
