from __future__ import annotations
import types
from attr import attrs, attrib, make_class
from datetime import datetime, timezone
import edgedb
from typing import Optional
from uuid import UUID
import edgewise
from enum import IntEnum


@attrs
class CustomScalar:
    __edbmodule__ = attrib(default=None, type=Optional[str])

    def pack(self):
        pass

    def unpack(self):
        pass


class DefaultEnum(IntEnum):
    @classmethod
    def default(self):
        default = [member for member in self.__members__ if member == self._default]
        return default[0] if default else None

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', value={self.value}, default={self.name == self._default})"
