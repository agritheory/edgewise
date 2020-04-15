from attr import attrs, attrib
import edgewise
import typing

import pytest


@edgewise.register
class DocumentNotInDatabase(edgewise.Document):
    def connect_to_filesystem(self) -> typing.NoReturn:
        pass


@edgewise.register_with_schema(module="example")
class Company(edgewise.Document):
    def your_class_method(self) -> str:
        return "A class method method!"


@pytest.mark.asyncio
async def test_DocumentNotInDatabase():
    doc = edgewise.new_doc("DocumentNotInDatabase")
    assert isinstance(doc, type(DocumentNotInDatabase))


@pytest.mark.asyncio
async def test_Company():
    doc = edgewise.new_doc("Company")
    assert hasattr(doc, 'your_class_method')
