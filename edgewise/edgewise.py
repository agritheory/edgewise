from __future__ import annotations
import typing
from edgewise.registry import ClassRegistry
from edgewise.document import Document
from uuid import UUID

class_registry = ClassRegistry()


def connect():  # -> edgedb.blocking
    global class_registry
    return class_registry.database


def new_doc(cls: str, *args, **kwargs) -> Document:
    global class_registry
    return class_registry.new_doc(cls, *args, **kwargs)


def get_doc(cls: str, filters: typing.Union[UUID, dict]) -> Document:
    global class_registry
    _doc = class_registry.new_doc(cls)
    return _doc._load(filters)


def get_all(cls: str, filters=None) -> typing.Sequence[UUID]:
    return


def register(class_definition, *args, **kwargs):
    global class_registry
    class_registry.register(class_definition.__name__, class_definition)
    return class_definition


def register_with_schema(module: str):
    def wrapped_registration(class_definition, *args, **kwargs):
        global class_registry
        class_registry.merge_class(module, class_definition)
        return class_definition
    return wrapped_registration
