import pytest
from edgewise import EdgeDBConnection


def is_responsive(url):
    try:
        conn = EdgeDBConnection()
    except Exception:
        return False


@pytest.fixture(scope="session", autouse=True)
def edgedb_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    return url
