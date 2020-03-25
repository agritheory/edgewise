from __future__ import annotations

import types
from datetime import datetime, timezone
from enum import IntEnum
from typing import Optional
from uuid import UUID

import edgedb
from attr import attrib, attrs, make_class


@attrs
class CustomScalar:
    __edbmodule__ = attrib(default=None, type=Optional[str])

    def pack(self):
        pass

    def unpack(self):
        pass


class DefaultEnum(IntEnum):
    __edbmodule__: Optional[str] = None

    @classmethod
    def default(self):
        default = [member for member in self.__members__ if member == self._default]
        return default[0] if default else None

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', value={self.value}, default={self.name == self._default})"


@attrs
class TupleScalar:
    __edbmodule__ = attrib(default=None, type=Optional[str])

    def pack(self):
        pass

    def unpack(self):
        pass


@attrs
class NamedTupleScalar:
    __edbmodule__ = attrib(default=None, type=Optional[str])

    def pack(self):
        pass

    def unpack(self):
        pass
