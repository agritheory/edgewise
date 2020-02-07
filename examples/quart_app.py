from quart import Quart, current_app
from dotenv import load_dotenv
from example import connect_to_example_db
import os


def create_app():
    load_dotenv()
    quart_app = Quart(__name__)
    quart_app.secret_key = os.getenv("SECRET")
    quart_app.db = connect_to_example_db()
    # quart_app.class_registry =
    return quart_app
