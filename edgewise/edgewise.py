from __future__ import annotations

import asyncio
import typing
from uuid import UUID
import warnings
from attr import attrs
import wrapt

from .document import Document
from .view import EdgeDBView
from .registry import ClassRegistry
from .scalars import CustomScalar, DefaultEnum


class_registry = ClassRegistry()


def new_doc(cls: str, *args, **kwargs) -> Document:
    global class_registry
    return class_registry.new_doc(cls, *args, **kwargs)


async def get_doc(cls: str, filters: typing.Union[UUID, dict]) -> Document:
    global class_registry
    _doc = class_registry.new_doc(cls)
    return await _doc._load(filters)


# @wrapt.decorator
def register(class_definition: typing.Type[Any], *args, **kwargs):
    global class_registry
    print("REGISTERING " + class_definition.__name__)
    class_registry.register(class_definition.__name__, attrs(class_definition))
    return class_definition(*args, **kwargs)


def register_with_schema(module: str):
    @wrapt.decorator
    def wrapped_registration(class_definition: typing.Type[Any], instance: typing.Type[Any], *args, **kwargs):
        global class_registry
        print("REGISTER WITH SCHEMA " + class_definition.__name__)
        class_registry.merge_class(module, attrs(class_definition))
        return class_definition(*args, **kwargs)

    return wrapped_registration


def new_scalar(scalar: str, *args, **kwargs) -> Document:
    global class_registry
    return class_registry.new_scalar(scalar, *args, **kwargs)


def register_scalar(scalar_definition: typing.Type[Any], *args, **kwargs):
    global class_registry
    class_registry._register_scalar(scalar_definition.__name__, scalar_definition)
    return scalar_definition


def register_scalar_with_schema(module: str):
    @wrapt.decorator
    def wrapped_registration(scalar_definition: typing.Type[Any], instance: typing.Type[Any], *args, **kwargs):
        global class_registry
        print("MERGING SCALAR " + scalar_definition.__name__)
        class_registry.merge_custom_scalar(module, attrs(scalar_definition))
        return scalar_definition

    return wrapped_registration


async def get_all(cls: str, filters=None) -> typing.Sequence[UUID]:
    warnings.warn(
        "edgewise.get_all is not yet implemented and is here to reserve namespace"
    )
    return


async def get_view(cls: str, filters=None) -> EdgeDBView:
    warnings.warn(
        "edgewise.get_view is not yet implemented and is here to reserve namespace"
    )
    return
