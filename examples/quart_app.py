from quart import Quart
import edgewise
from attr import attrs


app = Quart(__name__)


@app.before_serving
async def create_registry():
    await edgewise.class_registry.registration()


@app.route("/")
async def index() -> str:
    new_doc = edgewise.new_doc("Company")
    doc = await edgewise.get_doc('Company', {'name': 'Fancy Business'})
    # return str(dir(doc))
    return f"{doc.__repr__} {doc.your_class_method()}"


def register_custom_class():
    print('registering custom class')
    @attrs
    @edgewise.register_with_schema(module='example')
    class Company(edgewise.Document):
        def your_class_method(self) -> str:
            return "A class method method!"


register_custom_class()
app.run()
