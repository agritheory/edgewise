from attr import attrs, attrib
import edgewise
from edgewise import Document, register, register_with_schema
import typing


@attrs
@register
class DocumentNotInDatabase(Document):
    def connect_to_filesystem(self) -> typing.NoReturn:
        pass


@attrs
@register_with_schema(module='example')
class Company(Document):
    def your_class_method(self) -> str:
        return "A class method method!"
