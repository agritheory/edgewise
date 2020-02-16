from __future__ import annotations

import types
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

import edgedb
from attr import attrib, attrs, make_class

import edgewise
from edgewise.queries import insert_query, update_query, load_query


@attrs
class Document:
    __createdutc__ = attrib(default=None, type=Optional[datetime])
    __modifiedutc__ = attrib(default=None, type=Optional[datetime])
    __edbmodule__ = attrib(default=None, type=Optional[str])
    # __state__ = attrib(default=None, type=Optional[typing.Enum])
    _id = attrib(default=None, type=Optional[UUID])

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def _id_is_immutable(self, attribute, value):
        raise AttributeError()

    async def _load(self, filters: typing.Optional[dict]) -> Document:
        conn = await edgewise.class_registry.connect("async")
        data = await conn.fetchall(load_query(self, filters))
        if not data:
            return None
        data = data[0] if isinstance(data, edgedb.Set) else data
        super(Document, self).__setattr__("_id", getattr(data, "id"))
        {
            super(Document, self).__setattr__(field, getattr(data, field))
            for field in self.__fields__
            if field != "id"
        }
        return self

    async def save(self) -> Document:
        if not self.id:
            self.__modifiedutc__ = datetime.utcnow()
            self.__createdutc__ = datetime.utcnow()
            query = insert_query(self)
        else:
            self.__modifiedutc__ = datetime.utcnow()
            query = update_query(self)
        conn = await edgewise.class_registry.connect("async")
        async with conn.transaction():
            await conn.execute(query)

    async def delete(self):
        await self._delete()

    async def _delete(self) -> typing.NoReturn:
        delete_query = f"""WITH MODULE {self.__edbmodule__}
            DELETE {self.__class__.__name__}
            FILTER .id = <uuid>'{self.id}'
        """
        conn = await edgewise.class_registry.connect("async")
        async with conn.transaction():
            await conn.execute(delete_query)

    @property
    def __fields__(self) -> typing.List[str]:
        return [
            field
            for field in dir(self)
            if not field.startswith("_")
            and not isinstance(self.__getattribute__(field), types.MethodType)
        ]

    async def __aiter__(self) -> typing.Iterable[str]:
        for field in self.__fields__:
            yield self.__getattribute__(field)

    # def __iter__(self) -> typing.Iterable[str]:
    #     for field in self.__fields__:
    #         yield self.__getattribute__(field)

    async def items(self) -> typing.Iterable[tuple]:
        for field in self.__fields__:
            yield (field, self.__getattribute__(field))
