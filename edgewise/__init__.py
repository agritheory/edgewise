from __future__ import annotations

from .connections import EdgeDBConnection
from .edgewise import (
    CustomScalar,
    DefaultEnum,
    Document,
    class_registry,
    connect,
    get_doc,
    new_doc,
    new_scalar,
    register,
    register_scalar,
    register_scalar_with_schema,
    register_with_schema,
)
from .registry import ClassRegistry

__version__ = "0.1.0"
