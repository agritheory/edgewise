import dotenv
import os
import edgedb

# from edgedbdoc import Document


def connect_to_example_db():
    dotenv.load_dotenv()
    print(
        os.getenv("EDGEDB_HOST"),
        os.getenv("EDGEDB_USER"),
        os.getenv("EDGEDB_PASSWORD"),
        os.getenv("EDGEDB_DATABASE"),
    )
    return edgedb.connect(
        host=os.getenv("EDGEDB_HOST", default="localhost"),
        # port=os.getenv('EDGEDB_PORT', default=5656),
        # admin=os.getenv('EDGEDB_ADMIN', default=False),
        user=os.getenv("EDGEDB_USER", default="edgedb"),
        password=os.getenv("EDGEDB_PASSWORD"),
        database=os.getenv("EDGEDB_DATABASE", default="example"),
        # timeout=os.getenv('EDGEDB_TIMEOUT', default=60),
    )


# class User(Document):
#     # @save  # https://stackoverflow.com/questions/11731136/python-class-method-decorator-with-self-arguments
#     def encrypt_password(self):
#         pass
