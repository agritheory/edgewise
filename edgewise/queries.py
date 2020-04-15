from __future__ import annotations

import typing
from collections import namedtuple

import edgedb


def load_query(doc, filters) -> edgedb.Object:
    if ("id", "uuid") in filters:
        uuid = filters.get("uuid") or filters.get("id")
        fields = ",\n\t".join(doc.__fields__)
        load_query = f"""
            WITH MODULE {doc.__edbmodule__}
            SELECT {doc.__class__.__name__} {{
                {fields}
            }}
            FILTER .id = {uuid} LIMIT 1;"""
        return load_query
    elif filters:
        fields = ",\n\t".join(doc.__fields__)
        filters = " AND ".join({f".{k} = '{v}'" for k, v in filters.items()})
        load_query = f"""
            WITH MODULE {doc.__edbmodule__}
            SELECT {doc.__class__.__name__} {{
                {fields}
            }}
            FILTER {filters};"""
        return load_query
    else:
        raise edgedb.MissingArgumentError


def insert_query(doc):
    query = f"WITH MODULE {doc.__edbmodule__} INSERT {doc.__class__.__name__} {{ \n"
    for k, v in doc.items():
        query += insert_attribute(doc, k, v, query)
    return query + "\n};"


def update_query(doc):
    values = ""
    for k, v in doc.items():
        values += insert_attribute(doc, k, v, query)
    return f"""
        WITH MODULE {doc.__edbmodule__}
        UPDATE {doc.__class__.__name__}
        FILTER .id = <uuid>'{doc.id}'
        SET {{
            {values}
        }};
    """


def insert_attribute(doc, k: str, v: typing.Optional[typing.Any], query: str):
    if not v or k in ("id", "_id"):  # let EdgeDB assign object's UUID
        return ""
    elif isinstance(v, (set, list, edgedb.Array)):  # multi link Document
        subquery = "".join([nested_multi_link(list_item) for list_item in v])
        return f"\t{k} := {subquery},\n"
    elif hasattr(v, "__edbmodule__") and v.__module__ == "edgewise.registry":
        # single linked class inherited from Document
        return f"\t{k} := {nested_single_link(v)},\n"
    # elif isinstance(v, tuple):
    #     pass  # wip
    else:
        return f"\t{k} := '{v}',\n"


def nested_single_link(doc):
    if doc.id:
        return f"""
        (
            SELECT {doc.__class__.__name__}
            FILTER .id = <uuid>'{doc.id}'
        )"""
    else:
        query = f""" (
            INSERT {doc.__class__.__name__}  {{
        """
        for k, v in doc.items():
            query += insert_attribute(doc, k, v, query)
        return query + "\t\t}\n\t)"


def nested_multi_link(doc):
    pass


def object_schema(filter: str = "") -> str:
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
    }
    """
    return (
        schema_query + filter
        if filter
        else schema_query + "\nFILTER " + NON_STANDARD_OBJECTS
    )


def enum_schema() -> str:
    return (
        """
    WITH MODULE schema
    SELECT ScalarType {
        name,
        default,
        enum_values,
        annotations: { name, @value },
        constraints: { name },
    }
    FILTER EXISTS .enum_values"""
        + " AND "
        + NON_STANDARD_OBJECTS
    )


def custom_scalar_schema() -> str:
    return (
        """
    WITH MODULE schema
    SELECT ScalarType {
        name,
        default,
        annotations: { name, @value },
        constraints: { name },
    }
    FILTER NOT EXISTS .enum_values AND """
        + NON_STANDARD_OBJECTS
    )


NON_STANDARD_OBJECTS = """NOT contains(.name, 'cfg::')
AND NOT contains(.name, 'schema::')
AND NOT contains(.name, 'std::')
AND NOT contains(.name, 'stdgraphql::')
AND NOT contains(.name, 'sys::')
AND NOT contains(.name, 'cal::');"""
