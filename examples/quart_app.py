from quart import Quart
import edgewise
from attr import attrs


app = Quart(__name__)


@app.before_serving
def create_registry():
    edgewise.class_registry.registration()


@app.route("/")
async def index() -> str:
    new_doc = edgewise.new_doc("Company")
    doc = await edgewise.get_doc("Company", {"name": "Fancy Business"})
    return f"{doc.__repr__} {doc.your_class_method()}"


@attrs
@edgewise.register_with_schema(module="example")
class Company(edgewise.Document):
    def your_class_method(self) -> str:
        return "A class method method!"


app.run()
