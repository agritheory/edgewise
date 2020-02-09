from __future__ import annotations
from attr import attrs, attrib, make_class
import edgedb
import enum
import dotenv
import os
import typing
from .document import Document
from .edb_utils import type_map
from edgewise.utils import connect_sync
from edgewise.queries import object_schema, enum_schema, custom_scalar_schema
from edgewise.scalars import DefaultEnum, CustomScalar


@attrs  # (frozen=True)
class ClassRegistry:
    registry = attrib(default={})
    database = attrib(default=None)
    scalars = attrib(default={})
    repr_timestamps = attrib(default=False)

    def __attrs_post_init__(self, connection: typing.Optional[edgedb.BlockingIOConnection] = None) -> typing.NoReturn:
        self.database = connect_sync() if not connection else connection
        self.build_classes(self.get_object_schema())
        self.build_enums(self.get_enum_schema())
        self.build_custom_scalars(self.get_custom_scalar_schema())
        # scalars += self.build_collections(self.get_collections_schema())

    # def mutate(self, key, value):  # better name update?
    #     return attr.evolve(self, key=value)
    def new_doc(self, key: str, *args, **kwargs):
        cls = self.registry[key]
        return cls(*args, **kwargs)

    def new_scalar(self, key: str, *args, **kwargs):
        cls = self.scalars[key]
        if issubclass(cls, enum.Enum):
            return cls
        return cls(*args, **kwargs)

    def register(self, key: str, cls: type) -> typing.NoReturn:
        self.registry[key] = cls

    def _register_scalar(self, key: str, cls: type) -> typing.NoReturn:
        print(key)
        self.scalars[key] = cls

    def get_object_schema(self, module: typing.Optional[str] = None, object: typing.Optional[str] = None):
        if object:
            module = module if module else "default"
            filter = f"\nFILTER .name = '{module}::{object}' LIMIT 1;" if object else ""
            return self.database.fetchall(object_schema(filter))
        return self.database.fetchall(object_schema())

    def get_enum_schema(self, module: typing.Optional[str] = None, enum: typing.Optional[str] = None):
        return self.database.fetchall(enum_schema())

    def get_custom_scalar_schema(self, module: typing.Optional[str] = None, scalar: typing.Optional[str] = None):
        return self.database.fetchall(custom_scalar_schema())

    def get_custom_collection_schema(self, module: typing.Optional[str] = None, collection: typing.Optional[str] = None):
        return self.database.fetchall(collection_schema())

    def build_classes(self, objects) -> typing.NoReturn:
        for obj in objects:
            object_module, object_name = obj.name.split("::")
            attributes = self._build_attributes(obj)
            new_class = make_class(object_name, attributes, bases=(Document,))
            self.register(object_name, new_class)

    def merge_class(self, module, class_definition) -> typing.NoReturn:
        obj = self.get_object_schema(module=module, object=class_definition.__name__)[0]
        attributes = self._build_attributes(obj)
        new_class = make_class(
            class_definition.__name__, attributes, bases=(class_definition,)
        )
        self.register(class_definition.__name__, new_class)

    def _build_attributes(self, obj: edgedb.Object) -> dict:
        object_module, object_name = obj.name.split("::")
        attributes = {}
        attributes["__edbmodule__"] = attrib(default=object_module, type=str, repr=False)
        for prop in obj.properties:
            if 'tuple' in prop.target.name:
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
            attributes["__edbmodule__"] = attrib(default=scalar_module, type=str, repr=True)
            attributes['value'] = attrib(default=None, type=typing.Optional[str])
            attributes['default'] = attrib(default=default, type=typing.Optional[str])
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
        attributes['value'] = attrib(default=None, type=typing.Optional[str])
        attributes['default'] = attrib(default=default, type=typing.Optional[str])
        new_class = make_class(
            scalar_definition.__name__, attributes, bases=(scalar_definition,)
        )
        self._register_scalar(scalar_definition.__name__, new_class)
