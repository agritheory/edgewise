import pytest
import sys
import typing


@pytest.mark.skip
def test_globals() -> typing.NoReturn:
    edgewise_module = sys.modules["edgewise"]
    assert edgewise_module.class_registry is not None
    # assert globals()['edgewise']['class_registry'] is not None
