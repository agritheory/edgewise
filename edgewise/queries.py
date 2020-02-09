from __future__ import annotations
import typing
import edgedb


def insert_query(doc):
    query = (
        f"WITH MODULE {doc.__edbmodule__} INSERT {doc.__class__.__name__} {{ \n"
    )
    for k, v in doc.items():
        query += insert_attribute(doc, k, v, query)
    return query + "\n};"


def update_query(doc):
    values = ''
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
        return ''
    elif isinstance(v, (set, list, edgedb.Array)):  # multi link Document
        sub_query = ''.join([nested_multi_link(list_item) for list_item in v])
        return f"\t{k} := {subquery},\n"
    elif hasattr(v, '__edbmodule__') and v.__module__ == 'edgewise.registry':
        # single linked class inherited from Document
        return f"\t{k} := {nested_single_link(v)},\n"
    elif isinstance(v, (tuple, namedtuple)):
        pass  # wip
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
