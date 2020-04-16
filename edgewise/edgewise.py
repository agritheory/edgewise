from __future__ import annotations

import asyncio
import sys
import typing
import warnings
from uuid import UUID

from attr import attrs

import edgewise

from .connections import EdgeDBConnection
from .registry import ClassRegistry
from .scalars import CustomScalar, DefaultEnum
from .view import EdgeDBView

_edgewise_module = globals()["edgewise"]


def init_class_registry(connection: EdgeDBConnection, **kwargs) -> ClassRegistry:
    if _edgewise_module.class_registry is None:
        _edgewise_module.class_registry = ClassRegistry(connect=connection, **kwargs)
    else:
        raise RuntimeError(
            f"Registry is already bound to {_edgewise_module.class_registry}"
        )
    return _edgewise_module.class_registry  # type: ignore


def new_doc(cls: str, *args, **kwargs) -> edgewise.Document:
    return _edgewise_module.class_registry.new_doc(cls, *args, **kwargs)


async def get_doc(cls: str, filters: typing.Union[UUID, dict]) -> edgewise.Document:
    _doc = _edgewise_module.class_registry.new_doc(cls)
    return await _doc._load(filters)


def register(class_definition: typing.Type[typing.Any], *args, **kwargs):
    _edgewise_module.class_registry.register(
        class_definition.__name__, attrs(class_definition)
    )
    return class_definition(*args, **kwargs)


def register_with_schema(module: str):
    def wrapped_registration(
        class_definition: typing.Type[typing.Any], *args, **kwargs
    ):
        _edgewise_module.class_registry.merge_class(module, attrs(class_definition))
        return class_definition(*args, **kwargs)

    return wrapped_registration


def new_scalar(scalar: str, *args, **kwargs):
    return _edgewise_module.class_registry.new_scalar(scalar, *args, **kwargs)


def register_scalar(scalar_definition: typing.Type[typing.Any], *args, **kwargs):
    _edgewise_module.class_registry._register_scalar(
        scalar_definition.__name__, scalar_definition
    )
    return scalar_definition


def register_scalar_with_schema(module: str):
    def wrapped_registration(
        scalar_definition: typing.Type[typing.Any], *args, **kwargs
    ):
        _edgewise_module.class_registry.merge_custom_scalar(
            module, attrs(scalar_definition)
        )
        return scalar_definition

    return wrapped_registration


async def get_all(cls: str, filters=None) -> None:  # typing.Sequence[UUID]:
    warnings.warn(
        "edgewise.get_all is not yet implemented and is here to reserve namespace"
    )
    return


async def get_view(cls: str, filters=None) -> None:  # EdgeDBView:
    warnings.warn(
        "edgewise.get_view is not yet implemented and is here to reserve namespace"
    )
    return
