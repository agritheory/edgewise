from attr import attrs, attrib
import edgewise
from edgewise import CustomScalar, register_scalar, register_scalar_with_schema
import typing

import pytest


@register_scalar
class RandomScalar(CustomScalar):
    def print_something(self):
        return f"Something!"


@register_scalar_with_schema(module="example")
class Password(CustomScalar):
    def __str__(self):
        return f"Password(******)"

    def __repr__(self):
        return f"Password(******)"


@pytest.mark.asyncio
async def test_random_scalar():
    random_scalar = edgewise.new_doc("RandomScalar")
    assert random_scalar.print_something() == "Something!"


# @pytest.mark.usefixtures('class_registry')
@pytest.mark.asyncio
async def test_register_scalar_with_schema():
    # edgewise.class_registry = class_registry
    custom_scalar = edgewise.new_scalar("Password")
    custom_scalar = "mypassword"
    assert custom_scalar.__str__() == "Password(******)"


# add test for enum

# add test for tuple

# add test for named tuple

# add test for array
