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
        timeout=60
    )


@pytest.fixture(scope='session')
def connection_object():
    return get_connection_object()


@pytest.fixture(scope="session")
def class_registry():
    edgewise.class_registry = edgewise.ClassRegistry(
        connect=get_connection_object()
    )
    print(edgewise.class_registry)
