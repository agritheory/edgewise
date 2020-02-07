from __future__ import annotations
from attr import attrs, attrib, make_class
import edgedb
from pathlib import Path
from typing import Optional, Hashable
import dotenv
import os
import typing
from .document import Document
from .edb_utils import type_map


@attrs  # (frozen=True)
class ClassRegistry:
    registry = attrib(default={})
    database = attrib(default=None)
    filepath = attrib(default=None)
    modules = attrib(default=None)

    def __attrs_post_init__(self) -> typing.NoReturn:
        classes = self.inspect_db()
        if classes:
            self.build_classes(classes)

    # def mutate(self, key, value):
    #     return attr.evolve(self, key=value)

    def register(self, key: str, cls: type) -> typing.NoReturn:
        self.registry[key] = cls

    def connect(self, connection=None):
        dotenv.load_dotenv()
        return edgedb.connect(
            host=os.getenv("EDGEDB_HOST", default="localhost"),
            user=os.getenv("EDGEDB_USER", default="edgedb"),
            password=os.getenv("EDGEDB_PASSWORD"),
            database=os.getenv("EDGEDB_DATABASE", default="example"),
        )

    def inspect_db(self, connection=None, module=None, object=None):
        self.database = self.connect() if not connection else connection
        if object:
            module = module if module else "default"
            filter = f"\nFILTER .name = '{module}::{object}';" if object else ""
            return self.database.fetchall(schema_query + filter)
        return self.database.fetchall(schema_query + non_standard_objects)

    def build_classes(self, objects) -> typing.NoReturn:
        for obj in objects:
            object_module, object_name = obj.name.split("::")
            attributes = self._build_attributes(obj)
            new_class = make_class(object_name, attributes, bases=(Document,))
            self.register(object_name, new_class)

    def merge_class(self, class_definition) -> typing.NoReturn:
        obj = self.inspect_db(object=class_definition.__name__)
        attributes = self._build_attributes(obj)
        new_class = make_class(object_name, attributes, bases=(class_definition,))
        self.register(object_name, new_class)

    def _build_attributes(self, obj: edgedb.Object) -> dict:
        object_module, object_name = obj.name.split("::")
        attributes = {}
        attributes["__edbmodule__"] = attrib(default=object_module, type=str)
        for prop in obj.properties:
            prop_type = type_map.get(prop.target.name.split("::")[1])
            if prop.name in ("id"):
                continue
            attributes[prop.name] = attrib(default=None, type=prop_type)
            # need a repr=**obfuscated** for password scalar
            # password = attrib(repr=lambda value: '***')
        for link in obj.links:
            if link.name == "__type__":
                continue
            link_type = typing.Optional[link.target.name.split("::")[1]]
            if link.cardinality == "MANY":
                link_type = typing.Optional[typing.List[link_type]]
            attributes[link.name] = attrib(default=None, type=link_type)
        return attributes

    def new_doc(self, key, *args, **kwargs):
        cls = self.registry[key]
        return cls(*args, **kwargs)


schema_query = """
WITH MODULE schema
SELECT ObjectType {
    name,
    is_abstract,
    is_final,
    bases: { name },
    ancestors: { name },
    annotations: { name, @value },
    links: {
        name,
        cardinality,
        required,
        target: { name },
    },
    properties: {
        name,
        cardinality,
        required,
        target: { name },
    },
    constraints: { name },
    indexes: { name, expr },
}"""

non_standard_objects = """
FILTER NOT contains(.name, 'cfg::')
AND NOT contains(.name, 'schema::')
AND NOT contains(.name, 'std::')
AND NOT contains(.name, 'stdgraphql::')
AND NOT contains(.name, 'sys::');"""
