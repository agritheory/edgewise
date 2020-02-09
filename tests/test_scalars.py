from attr import attrs, attrib
import edgewise
from edgewise import CustomScalar, register_scalar, register_scalar_with_schema
import typing


@attrs
@register_scalar
class RandomScalar(CustomScalar):
    def print_somthing(self):
        return f"Something!"


@attrs
@register_scalar_with_schema(module='example')
class Password(CustomScalar):
    def print_password(self):
        return f"Password(******)"
