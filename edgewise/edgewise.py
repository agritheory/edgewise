from __future__ import annotations

import asyncio
import typing
from uuid import UUID

from edgewise.document import Document
from edgewise.registry import ClassRegistry
from edgewise.scalars import CustomScalar, DefaultEnum

class_registry = ClassRegistry()


def connect(action: str = 'async') -> typing.Union[edgedb.BlockingIOConnection, edgedb.AsyncIOConnection]:
    return class_registry.connect(action)


def new_doc(cls: str, *args, **kwargs) -> Document:
    global class_registry
    return class_registry.new_doc(cls, *args, **kwargs)


async def get_doc(cls: str, filters: typing.Union[UUID, dict]) -> Document:
    global class_registry
    _doc = class_registry.new_doc(cls)
    return await _doc._load(filters)


def get_all(cls: str, filters=None) -> typing.Sequence[UUID]:
    return


def register(class_definition: typing.Type[Any], *args, **kwargs):
    global class_registry
    class_registry.register(class_definition.__name__, class_definition)
    return class_definition


def register_with_schema(module: str):
    def wrapped_registration(class_definition: typing.Type[Any], *args, **kwargs):
        global class_registry
        class_registry.merge_class(module, class_definition)
        return class_definition

    return wrapped_registration


def new_scalar(scalar: str, *args, **kwargs) -> Document:
    global class_registry
    return class_registry.new_scalar(scalar, *args, **kwargs)


def register_scalar(scalar_definition: typing.Type[Any], *args, **kwargs):
    global class_registry
    class_registry._register_scalar(scalar_definition.__name__, scalar_definition)
    return scalar_definition


def register_scalar_with_schema(module: str):
    def wrapped_registration(scalar_definition: typing.Type[Any], *args, **kwargs):
        global class_registry
        class_registry.merge_custom_scalar(module, attrs(scalar_definition))
        return scalar_definition

    return wrapped_registration
