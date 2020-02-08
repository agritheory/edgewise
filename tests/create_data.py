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


def create_records(company=1, user=1, rbac_role=1):
    for i in range(0, company):
        create_company()
    for i in range(0, user):
        create_user()
    for i in range(0, rbac_role):
        create_rbac_role()


def create_company():
    company = edgewise.new_doc("Company")
    company.name = mimesis.Person("en").last_name() + " " + mimesis.Business().company_type(abbr=True)
    company.country = "United States"
    company.save()


def create_user():
    person = mimesis.Person("en")
    user = edgewise.new_doc("User")
    user.first_name = person.name()
    user.last_name = person.last_name()
    user.email = person.email()
    user.password = person.password()
    user.username = person.username()
    user.save()


def create_rbac_role():
    role = edgewise.new_doc("RBACRole")
    role.name = mimesis.Person("en").occupation().replace(' ', '')
    role.save()
