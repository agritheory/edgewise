import datetime
import decimal
import typing
import uuid

import edgedb

type_map = {
    "array": typing.Optional[edgedb.Array],
    "uuid": typing.Optional[uuid.UUID],
    "str": typing.Optional[str],
    "json": typing.Optional[str],
    "anyenum": typing.Optional[str],
    "bool": typing.Optional[bool],
    "float32": typing.Optional[float],
    "float64": typing.Optional[float],
    "int16": typing.Optional[int],
    "int32": typing.Optional[int],
    "int64": typing.Optional[int],
    "decimal": typing.Optional[decimal.Decimal],
    "bytes": typing.Optional[bytes],
    "local_date": typing.Optional[datetime.date],
    "local_time": typing.Optional[datetime.time],
    "local_datetime": typing.Optional[datetime.datetime],
    "datetime": typing.Optional[datetime.datetime],
    "duration": typing.Optional[datetime.timedelta],
    "Object": typing.Optional[edgedb.Object],
}
