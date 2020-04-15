from __future__ import annotations

from .connections import EdgeDBConnection
from .document import Document
from .edgewise import (
    get_doc,
    init_class_registry,
    new_doc,
    new_scalar,
    register,
    register_scalar,
    register_scalar_with_schema,
    register_with_schema,
)
from .registry import ClassRegistry
from .scalars import CustomScalar, DefaultEnum

class_registry = None

__version__ = "0.1.0"
