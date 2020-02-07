import asyncio
import click
import edgedb
import mimesis
from examples.example import connect_to_example_db
import dotenv
import os
import edgewise


user_schema = """
CREATE MIGRATION init_user TO {
    MODULE example {
        type Company {
            required property name -> str;
            property country  -> str;
        }
        type RBACRole {
          required property name -> str;
        }
        type User {
            property first_name -> str;
            property last_name -> str;
            required property username -> str;
            required property password -> str;
            multi link company -> Company;
            multi link rbac_role -> RBACRole;
        }
    }
};
COMMIT MIGRATION init_user;
"""


@click.command()
def create_user_doctype():
    conn = connect_to_example_db()
    exists = conn.fetchall("""
            WITH x := (SELECT schema::Module {name}
            FILTER schema::Module.name = 'example') SELECT x.name;
        """)
    if not exists:
        conn.execute("CREATE MODULE example")
    with conn.transaction():
        conn.execute(user_schema)


def create_company():
    company = edgewise.new_doc("Company")
    company.name = mimesis.Person("en").last_name() + " " + mimesis.Business().company_type(abbr=True)
    company.country = "United States"
    return company


def create_user():
    person = mimesis.Person("en")
    user = edgewise.new_doc("User")
    user.first_name = person.name()
    user.last_name = person.last_name()
    user.email = person.email()
    user.password = person.password()
    user.username = person.username()
    return user
