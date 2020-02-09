# edge|wise

This library is designed to be used as an Active Record style Object Relational Mapper for [EdgeDB](https://edgedb.com). A `ClassRegistry` object is built from a combination of EdgeDB schema and the `@register` decorator, which allows for merging class definition and database schema. This means you're able to add an overlay of your own class methods and properties that otherwise wouldn't exist. New instances can be created by calling `edgewise.new_doc('Object')`. Existing objects can be fetched with `edgewise.get_doc('Object', uuid, filters)` using either the object's unique uuid or a dictionary of filters (`{'name': 'Magic'}`)

## Getting Started
### Prerequisites
This library uses python >3.7 and requires that EdgeDB be installed. Follow the [installation instructions](https://edgedb.com/docs/tutorial/install) given in the EdgeDB documentation.

This library ~~uses~~ will use asyncio by default and generally defers to it whenever possible.
### Why?
The EdgeDB python library is intended to be relatively low-level and highly performant. This library is designed to be intuitive and help you access and amipulate documents in relatively few steps, in a object oriented style. If you're doing a large application with EdgeDB you should be prepared to use both libraries. EdgeDB SDL is the among the most intuitive ways to define schema. This library take the approach that you should design your schema in its native language and access it in a way that's easiest for you.

### How it Works
This library first inspects your EdgeDB database with a schema query and builds classes from that with the help of the [attrs](www.attrs.org) library. In formal computer science this is called an Inversion of Control pattern. You can create a new python instance of a class by calling `edgewise.new_doc('Object')` where 'Object' is the name of your EdgeDB object. All edgewise classes inherit from `Document` which provides several useful abstractions for you.

### Basic Usage - Objects
```python
>>> import edgewise
>>> doc = edgewise.get_doc('Company', {'name':'Fancy Business'}) # schema defined here[]()
>>> doc # let's see it in the repl
Company(id=UUID('fbc7933e-49da-11ea-9634-efbf1f5f7fea'), __edbmodule__='example',
name='Fancy Business', country='Monaco') # that is fancy!
>>> doc.country = 'Cayman Islands' # assign a new value to the 'country' attribute
>>> doc.save()  # saves to the database, no fuss
>>> doc.delete() # gone forever
>>> new_company = edgewise.new_doc("Company")
>>> new_company
Company(id=None,__edbmodule__='example', name=None, country=None)
```
If you'd like to extend a database object you can do that with the help of some decorators.
**Note:** `@attrs` is required for inheritence to work correctly. To ensure version compatibility import `attrs` from `edgewise`.
```python
from edgewise import attrs, Document, register, register_with_schema

@attrs
@register_with_schema(module='example')
class Company(Document):
    def your_class_method(self) -> str:
        return "A class method method!"
```
`register_with_schema(module)` allows you add your own class methods to the object.
```python
>>> new_company = edgewise.new_doc("Company")
>>> new_company
Company(_id=None, __edbmodule__='example', name=None, country=None)
>>> new_company.test_this_class_method()
'A class method!'
```
You can also make classes that don't need database access available in the ClassRegistry:
```python
@attrs
@register
class DocumentNotInDatabase(Document):
    def connect_to_filesystem(self) -> typing.NoReturn:
        pass
```
In this case, you will probably want to provide the `edgewise` APIs you'd expect to see: `_load` (called by `get_doc`), `save` and `delete`; only `new_doc` will work out of the box.

### Basic Usage - Scalars and Enums
EdgeDB allows you define custom scalars and enums, Edgewise supports mapping these to python representations. Enums will use the Edgewise `DefaultEnum` class. Scalars will use the CustomScalar class. CustomScalars are extensible with a decorator. You can also put a custom object into the registry with  the `@register_scalar` decorator.

```python
@attrs
@register_scalar
class RandomScalar(CustomScalar):
    def print_somthing(self):
        return f"Something!"


@attrs
@register_scalar_with_schema(module='example')
class Password(CustomScalar):
    def print_password(self):
        return f"Password(******)"
```
Using this example enum definition will yield a python enum object with the ability to also store a default value.
```
scalar type Color extending enum<'black', 'white', 'red'>;
```
```python
>>> import edgewise
>>> colors = edgewise.new_scalar('Color')
>>> colors
<enum 'Color'>  # The default enum __repr__ is useless
>>> colors.black
Color(name='black', value=1, default=True) # this repr is provided by DefaultEnum
>>> colors.white
Color(name='white', value=2, default=False)
>>> colors.default()
'black'
```

### EdgeDB Configuration and Connectivity
**WIP**
You'll want to configure a user with administrative permissions. For example:

It is generally considered good practice to save database passwords as environmental variables.  


### Installing
This library is not yet on pypi
```bash
python -m pip install edgewise
```
If you've read this far you know that you should use a virtual environment and you should do that however you like. But you should do it. For development this project uses Pipenv until something better comes along, which has probably already happened.

## Developing with Edgewise
Have a look at [the roadmap](./roadmap.md), which is about as useful as a streetmap of Boston.

### Examples
Examples are available in the examples folder. Some of these will be covered in the tutorial documentation.

If you're considering integrating this library into a framework or project, please consider contributing your changes and/or add an example implementation to the test suite so that breaking changes can be discovered before they mess up your project.

## Dependencies and Tooling
For production code this project uses `attrs`, `python-dotenv` and the EdgeDB python client.
For testing and development: `pipenv`, `black`, `pytest` (and several plugins), and `ipython`. Please refer to the Pipfile for more information.

## Contributing

Contributions are welcome, please refer to the wiki regarding:
* Opening GitHub issues
* Requesting support

## Versioning
This project ~~uses~~ will use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/agritheory/edgewise/tags).

## Authors
* **Tyler Matteson** - *Initial work* - [AgriTheory](https://agritheory.com/)

## License
 See the [license.md](./license.md) file for details
