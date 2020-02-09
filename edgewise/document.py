from __future__ import annotations
import types
from attr import attrs, attrib, make_class
from datetime import datetime, timezone
import edgedb
from typing import Optional
from uuid import UUID
import edgewise
from edgewise.queries import insert_query, update_query


@attrs
class Document:
    # __createdutc__ = attrib(default=None, type=Optional[datetime])
    # __modifiedutc__ = attrib(default=None, type=Optional[datetime])
    __edbmodule__ = attrib(default=None, type=Optional[str])
    # __state__ = attrib(default=None, type=Optional[typing.Enum])
    _id = attrib(default=None, type=Optional[UUID])

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def _id_is_immutable(self, attribute, value):
        raise AttributeError()

    def _load(
        self, filters: Union[None, dict, UUID]
    ) -> Document:
        data = self._load_query(filters)
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

    def _load_query(self, filters) -> edgedb.Object:
        if isinstance(filters, UUID):
            fields = ",\n\t".join(self.__fields__)
            load_query = f"""
                WITH MODULE {self.__edbmodule__}
                SELECT {self.__class__.__name__} {{
                    {fields}
                }}
                FILTER .id = {uuid} LIMIT 1;"""
            return edgewise.connect().fetchall(load_query)
        elif filters:
            fields = ",\n\t".join(self.__fields__)
            filters = " AND ".join({f".{k} = '{v}'" for k, v in filters.items()})
            load_query = f"""
                WITH MODULE {self.__edbmodule__}
                SELECT {self.__class__.__name__} {{
                    {fields}
                }}
                FILTER {filters};"""
            return edgewise.connect().fetchall(load_query)
        else:
            raise edgedb.MissingArgumentError

    def save(self) -> Document:
        if not self.id:
            self.__modifiedutc__ = datetime.utcnow()
            self.__createdutc__ = datetime.utcnow()
            query = insert_query(self)
        else:
            self.__modifiedutc__ = datetime.utcnow()
            query = update_query(self)
        print(query)
        with edgewise.connect().transaction():
            edgewise.connect().execute(query)

    def delete(self):
        self._delete()

    def _delete(self) -> typing.NoReturn:
        delete_query = f"""WITH MODULE {self.__edbmodule__}
            DELETE {self.__class__.__name__}
            FILTER .id = <uuid>'{self.id}'
        """
        with edgewise.connect().transaction():
            edgewise.connect().execute(delete_query)

    @property
    def __fields__(self) -> typing.List[str]:
        return [
            field
            for field in dir(self)
            if not field.startswith("_")
            and not isinstance(self.__getattribute__(field), types.MethodType)
        ]

    def __iter__(self) -> typing.Iterable[str]:
        for field in self.__fields__:
            yield self.__getattribute__(field)

    def items(self) -> typing.Iterable[tuple]:
        for field in self.__fields__:
            yield (field, self.__getattribute__(field))
