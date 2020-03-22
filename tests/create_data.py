
import asyncio
import random

import edgedb
import mimesis
import pytest

import edgewise
from .conftest import get_connection_object


user_schema = """
CREATE MIGRATION init_user TO {
  MODULE example {
        scalar type Password extending str;
        scalar type Color extending enum<'black', 'white', 'red'>;
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
        property email -> str;
        required property username -> str;
        required property password -> Password;
        multi link company -> Company;
        multi link rbac_role -> RBACRole;
    }
  }
};
COMMIT MIGRATION init_user;
"""


def build_schema():
    connection_object = get_connection_object()
    conn = connection_object('sync')
    with conn.transaction():
        conn.execute(user_schema)


def create_registry():
    connection_object = get_connection_object()
    edgewise.class_registry = edgewise.ClassRegistry(connection_object)


def create_records(company=2, user=10, rbac_role=4, save=False):
    create_registry()
    asyncio.run(_create_records(company, user, rbac_role, save))


async def _create_records(company, user, rbac_role, save):
    companies, rbac_roles = [], []
    for i in range(0, company):
        companies.append(await create_company(save))
    for i in range(0, rbac_role):
        rbac_roles.append(await create_rbac_role(save))
    for i in range(0, user):
        company = random.choice(companies).name
        role = random.choice(rbac_roles).name
        await create_user(company, role, save)


async def create_company(save):
    company = edgewise.new_doc("Company")
    company.name = mimesis.Person("en").last_name() + " "\
        + mimesis.Business().company_type(abbr=True)
    company.country = "United States"
    print(company.name)
    if save:
        await company.save()
    return company


async def create_user(company, role, save):
    person = mimesis.Person("en")
    user = edgewise.new_doc("User")
    user.first_name = person.name()
    user.last_name = person.last_name()
    user.email = person.email()
    user.password = 'password'
    user.username = person.username()
    # user.rbac_role = role
    # user.company = company
    print(user.username)
    if save:
        await user.save()
    return user


async def create_rbac_role(save):
    role = edgewise.new_doc("RBACRole")
    role.name = mimesis.Person("en").occupation().replace(' ', '')
    print(role.name)
    if save:
        await role.save()
    return role
