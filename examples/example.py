import dotenv
import os
import edgedb

# from edgedbdoc import Document


def connect_to_example_db():
    dotenv.load_dotenv()
    return edgedb.connect(
        host=os.getenv("EDGEDB_HOST", default="localhost"),
        user=os.getenv("EDGEDB_USER", default="edgedb"),
        password=os.getenv("EDGEDB_PASSWORD"),
        database=os.getenv("EDGEDB_DATABASE", default="example"),
    )


# class User(Document):
#     # @save  # https://stackoverflow.com/questions/11731136/python-class-method-decorator-with-self-arguments
#     def encrypt_password(self):
#         pass
