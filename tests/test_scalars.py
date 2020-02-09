from attr import attrs, attrib
import edgewise
from edgewise import CustomScalar, register_scalar, register_scalar_with_schema
import typing


@attrs
@register_scalar
class SecretPassword(CustomScalar):
    def print_password(self):
        return f"Password(******)"


@attrs
@register_scalar_with_schema(module='example')
class Password(CustomScalar):
    def __repr__(self):
        return f"Password(******)"
