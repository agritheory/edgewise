from __future__ import annotations

# __all__ = ['new_doc', 'get_doc', 'register_class']
# __module__ = 'edgewise'
import functools
from .registry import ClassRegistry
from .document import Document


class_registry = ClassRegistry()


def connect():
    global class_registry
    return class_registry.database


def new_doc(cls, *args, **kwargs):
    global class_registry
    return class_registry.new_doc(cls, *args, **kwargs)


def get_doc(cls, uuid=None, filters=None):
    global class_registry
    if not uuid and not filters:
        raise TypeError("Either UUID or filters are required to retreive a document")
    _doc = class_registry.new_doc(cls)
    return _doc._load(uuid) if uuid else _doc._load(filters=filters)


def register(class_definition, *args, **kwargs):
    global class_registry
    class_registry.register(class_definition.__name__, class_definition)
    return class_definition


def register_with_schema(class_definition, *args, **kwargs):
    global class_registry
    class_registry.merge_class(class_definition)
    return class_definition
