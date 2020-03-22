from attr import attrs, attrib
import edgewise
from edgewise import CustomScalar, register_scalar, register_scalar_with_schema
import typing


@attrs
@register_scalar
class RandomScalar(CustomScalar):
    def print_something(self):
        return f"Something!"


@attrs
@register_scalar_with_schema(module='example')
class Password(CustomScalar):
    def print_password(self):
        return f"Password(******)"


@pytest.mark.usefixtures('class_registry')
@pytest.mark.asyncio
async def test_random_scalar():
    random_scalar = await edgewise.new_doc('RandomScalar')
    assert random_scalar.print_something() == 'Something!'


@pytest.mark.usefixtures('class_registry')
@pytest.mark.asyncio
async def test_register_scalar_with_schema():
    custom_scalar = await edgewise.new_scalar('Password')
    custom_scalar = 'mypassword'
    assert custom_scalar.__str__() == 'Password(******)'
