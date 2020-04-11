from attr import attrs, attrib
import edgewise
from edgewise import Document, register, register_with_schema
import typing

import pytest


@register
class DocumentNotInDatabase(Document):
    def connect_to_filesystem(self) -> typing.NoReturn:
        pass


@register_with_schema(module="example")
class Company(Document):
    def your_class_method(self) -> str:
        return "A class method method!"


@pytest.mark.asyncio
async def test_DocumentNotInDatabase():
    doc = edgewise.new_doc("DocumentNotInDatabase")
    assert isinstance(doc, type(DocumentNotInDatabase))


@pytest.mark.asyncio
async def test_Company():
    doc = edgewise.new_doc("Company")
    print(dir(doc))
    assert hasattr(doc, 'your_class_method')
