from __future__ import annotations

import enum
import os
import typing

import edgedb
from attr import attrib, attrs, make_class

from edgewise.connections import EdgeDBConnection
from edgewise.document import Document
from edgewise.edb_utils import type_map
from edgewise.queries import custom_scalar_schema, enum_schema, object_schema
from edgewise.scalars import CustomScalar, DefaultEnum


@attrs
class ClassRegistry:
    connect = attrib(default=None, type=EdgeDBConnection)
    registry = attrib(default={}, type=typing.Dict)
    scalars = attrib(default={}, type=typing.Dict)
    repr_timestamps = attrib(default=False, type=bool)

    def __attrs_post_init__(self) -> typing.NoReturn:
        if self.connect is not None:
            self.build_classes(self.get_object_schema())
            self.build_enums(self.get_enum_schema())
            self.build_custom_scalars(self.get_custom_scalar_schema())

    def new_doc(self, key: str, *args, **kwargs):
        cls = self.registry[key]
        return cls(*args, **kwargs)

    def new_scalar(self, key: str, *args, **kwargs):
        cls = self.scalars[key]
        if issubclass(cls, enum.Enum):
            return cls
        return cls(*args, **kwargs)

    def register(self, key: str, cls: type) -> typing.NoReturn:
        if not self.registry.get(key):
            self.registry[key] = cls

    def _register(self, key: str, cls: type) -> typing.NoReturn:
        if self.registry.get(key):
            self.registry.pop(key)
        self.registry[key] = cls

    def _register_scalar(self, key: str, cls: type) -> typing.NoReturn:
        self.scalars[key] = cls

    def get_object_schema(self):
        conn = self.connect("sync")
        objects = conn.fetchall(object_schema())
        conn.close()
        return objects

    def get_enum_schema(
        self, module: typing.Optional[str] = None, enum: typing.Optional[str] = None
    ):
        conn = self.connect("sync")
        enums = conn.fetchall(enum_schema())
        conn.close()
        return enums

    def get_custom_scalar_schema(
        self, module: typing.Optional[str] = None, scalar: typing.Optional[str] = None
    ):
        conn = self.connect("sync")
        scalars = conn.fetchall(custom_scalar_schema())
        conn.close()
        return scalars

    def build_classes(self, objects) -> typing.NoReturn:
        for obj in objects:
            object_module, object_name = obj.name.split("::")
            attributes = self._build_attributes(obj)
            new_class = make_class(object_name, attributes, bases=(Document,))
            self.register(object_name, new_class)

    def merge_class(self, module: str, class_definition: object) -> typing.NoReturn:
        filter = f"\nFILTER .name = '{module}::{class_definition.__name__}' LIMIT 1;"
        obj = self.connect("sync").fetchall(object_schema(filter))
        if not obj:
            self.register(class_definition.__name__, class_definition)
            return
        attributes = self._build_attributes(
            obj[0]
        )  # LIMIT 1 rerturns a Set of 1 object
        new_class = make_class(
            class_definition.__name__, attributes, bases=(class_definition,)
        )
        self._register(class_definition.__name__, new_class)

    def _build_attributes(self, obj: edgedb.Object) -> dict:
        object_module, object_name = obj.name.split("::")
        attributes = {}
        attributes["__edbmodule__"] = attrib(
            default=object_module, type=str, repr=False
        )
        for prop in obj.properties:
            if "tuple" in prop.target.name:
                prop_type = prop.target.name
            else:
                prop_type = type_map.get(prop.target.name.split("::")[1])
            if prop.name in ("id"):
                continue

            # if prop.name in ("id", "__edbmodule__"):
            #     attributes[prop.name] = attrib(default=None, type=prop_type, repr=self.repr_id_and_module)
            # if prop.name in ("__createdutc__", "__modifiedutc__"):
            #     attributes[prop.name] = attrib(default=None, type=prop_type, repr=self.repr_timestamps)
            attributes[prop.name] = attrib(default=None, type=prop_type)
        for link in obj.links:
            if link.name == "__type__":
                continue
            link_type = typing.Optional[link.target.name.split("::")[1]]
            if link.cardinality == "MANY":
                link_type = typing.Optional[typing.List[link_type]]
            attributes[link.name] = attrib(default=None, type=link_type)
        return attributes

    def build_enums(self, enums) -> typing.NoReturn:
        for enum in enums:
            enum_module, enum_name = enum.name.split("::")
            new_enum = DefaultEnum(enum_name, list(enum.enum_values))
            new_enum._default = enum.default if enum.default else enum.enum_values[0]
            new_enum.__edbmodule__ = enum_module
            if enum.annotations:
                new_enum.__doc__ = enum.annotations
            new_enum.__name__ = enum_name
            self._register_scalar(enum_name, new_enum)

    def build_custom_scalars(self, scalars) -> typing.NoReturn:
        for scalar in scalars:
            attributes = {}
            scalar_module, scalar_name = scalar.name.split("::")
            default = scalar.default if scalar.default else None
            attributes["__edbmodule__"] = attrib(
                default=scalar_module, type=str, repr=True
            )
            attributes["value"] = attrib(default=None, type=typing.Optional[str])
            attributes["default"] = attrib(default=default, type=typing.Optional[str])
            new_class = make_class(scalar_name, attributes, bases=(CustomScalar,))
            self._register_scalar(scalar_name, new_class)

    def merge_custom_scalar(self, module: str, scalar_definition) -> typing.NoReturn:
        scalar = self.get_custom_scalar_schema(
            module=module, scalar=scalar_definition.__name__
        )[0]
        attributes = {}
        scalar_module, scalar_name = scalar.name.split("::")
        default = scalar.default if scalar.default else None
        attributes["__edbmodule__"] = attrib(default=scalar_module, type=str, repr=True)
        attributes["value"] = attrib(default=None, type=typing.Optional[str])
        attributes["default"] = attrib(default=default, type=typing.Optional[str])
        new_class = make_class(
            scalar_definition.__name__, attributes, bases=(scalar_definition,)
        )
        self._register_scalar(scalar_definition.__name__, new_class)
