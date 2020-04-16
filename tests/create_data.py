import asyncio
from pathlib import Path
import csv

import edgedb

import edgewise


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


async def create_company():
    file_path = Path(__file__).parent / "company.csv"
    with open(file_path) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in csvreader:
            company = edgewise.new_doc("Company")
            company.name = row[0]
            company.country = row[1]
            await company.save()


async def create_user():
    file_path = Path(__file__).parent / "user.csv"
    with open(file_path) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in csvreader:
            print(row[0])
            user = edgewise.new_doc("User")
            user.first_name = row[0]
            user.last_name = row[1]
            user.email = row[2]
            user.password = "<raw_str>" + row[3]
            user.username = user.email
            user.company = await edgewise.get_doc("Company", {"name": row[4]})
            user.rbac_role = await edgewise.get_doc("RBACRole", {"name": row[5]})
            await user.save()


async def create_rbac_role():
    for role_name in ("Base User", "Guest", "Administrator"):
        role = edgewise.new_doc("RBACRole")
        role.name = role_name
        await role.save()
