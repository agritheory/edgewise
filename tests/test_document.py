from attr import attrs, attrib
import edgewise
from edgewise import Document, register, register_with_schema


@attrs
@register
class ExampleDocument(Document):
    pass


@attrs
@register_with_schema
class User(Document):
    def test_this_class_method(self):
        return 'testing this class method'
