from __future__ import annotations
import types
from attr import attrs, attrib, make_class
from datetime import datetime, timezone
import edgedb
from typing import Optional
from uuid import UUID
import edgewise


@attrs
class Document:
    __createdutc__ = attrib(default=None, type=Optional[datetime])
    __modifiedutc__ = attrib(default=None, type=Optional[datetime])
    __edbmodule__ = attrib(default=None, type=Optional[str])
    __createdby__ = attrib(default=None, type=Optional[str])
    __modifiedby__ = attrib(default=None, type=Optional[str])
    _id = attrib(default=None, type=Optional[UUID])

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def _id_is_immutable(self, attribute, value):
        raise AttributeError()

    def _load(self, uuid: Union[str, UUID, None] = None, filters: Optional[dict] = None) -> Document:
        data = self._load_query(uuid, filters)
        if not data:
            return None
        data = data if len(data) > 1 else data[0]  # or should return a list of documents?
        super(Document, self).__setattr__('_id', getattr(data, 'id'))
        {
            super(Document, self).__setattr__(
                field, getattr(data, field)) for field in self.__fields__ if field != 'id'
        }
        return self

    def _load_query(self, uuid, filters) -> edgedb.Object:
        if uuid:
            fields = ",\n\t".join(self.__fields__)
            load_query = f"""
                WITH MODULE {self.__edbmodule__}
                SELECT {self.__class__.__name__} {{
                    {fields}
                }}
                FILTER .id = {uuid};"""
            return edgewise.connect().fetchall(load_query)
        elif filters:
            fields = ",\n\t".join(self.__fields__)
            filters = ' AND '.join({f".{k} = '{v}'" for k, v in filters.items()})
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
        self._insert() if not self.id else self._update()

    def _insert(self) -> Document:
        if not self.__createdutc__:
            self.__createdutc__ = datetime.utcnow()
            self.__modifiedutc__ = self.__createdutc__
        insert = (
            f"WITH MODULE {self.__edbmodule__} INSERT {self.__class__.__name__} {{ \n"
        )
        insert += ",\n".join(f"\t{k} := \'{v}\'" for k, v in self.items() if k != 'id')
        insert += "\n};"
        with edgewise.connect().transaction():
            edgewise.connect().execute(insert)

    def _update(self) -> Document:
        self.__modifiedutc__ = datetime.utcnow()
        values = ",\n".join(f"\t{k} := '{v}'" for k, v in self.items() if k != "id")
        update = f"""WITH MODULE {self.__edbmodule__}
            UPDATE {self.__class__.__name__}
            FILTER .id = <uuid>'{self.id}'
            SET {{
                {values}
            }};"""
        with edgewise.connect().transaction():
            edgewise.connect().execute(update)

    def _delete(self) -> typing.NoReturn:
        delete_query = f"""WITH MODULE {self.__edbmodule__}
            DELETE {self.__class__.__name__}
            FILTER .id = <uuid>'{self.id}'
        """
        with edgewise.connect().transaction():
            edgewise.connect().execute(delete_query)

    @property
    def __fields__(self) -> typing.List[str]:
        return [field for field in dir(self) if not field.startswith("_")
            and not isinstance(self.__getattribute__(field), types.MethodType)]

    def __iter__(self) -> typing.Iterable[str]:
        for field in self.__fields__:
            yield self.__getattribute__(field)

    def items(self) -> typing.Iterable[tuple]:
        for field in self.__fields__:
            yield (field, self.__getattribute__(field))
