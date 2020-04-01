# edge|wise
[![CircleCI](https://circleci.com/gh/agritheory/edgewise.svg?style=shield)](https://circleci.com/gh/agritheory/edgewise) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


This library is designed to be used as an Active Record style Object Relational Mapper for [EdgeDB](https://edgedb.com). A `ClassRegistry` object is built from a combination of EdgeDB schema and the `@register` family of decorators, which allows for merging class definition and database schema. This means you're able to add an overlay of your own class methods and properties that otherwise wouldn't exist. New instances can be created by calling `edgewise.new_doc('Object')`. Existing objects can be fetched with `edgewise.get_doc('Object', filters)` using either the object's UUID or a dictionary of filters filtering on a property (`{'name': 'Magic'}`)

* Getting Started
  * Prerequisites
  * Why?
  * Installing
* Using Edgewise
  * How it Works
  * Basic Usage - Objects
  * Basic Usage - Enums and Custom Scalars
  * Basic Usage - Tuples and Named Tuples
  * Async is Awesome!
* EdgeDB Configuration
  * Environment Variables
  * Extras
    * Timestamping
    * Password Scalar
* Developing with Edgewise
  * Examples
    * Quart example
  * Dependencies and Tooling
  * About the Test Suite
  * Contributing
  * Versioning
  * Author(s)
  * License

## Getting Started
### Prerequisites
This library uses python >3.6 and requires that EdgeDB be installed. Follow the [installation instructions](https://edgedb.com/docs/tutorial/install) given in the EdgeDB documentation.

Edgewise is [asyncio](https://docs.python.org/3/library/asyncio.html) by default and generally defers to it whenever possible. See the [async is awesome](#async-is-awesome) and [Quart example](#quart-example) for more details.

### Why?
The EdgeDB python library is intended to be relatively low-level and high performance. This library is designed to be intuitive and help you access and manipulate documents quickly in a object oriented style. If you're doing a large application with EdgeDB you should be prepared to use both libraries.

In my experience, EdgeDB SDL is one of the most intuitive ways to define schema, especially one with nested objects/tables and types. This library takes the approach that you should design your schema in its native language (EdgeDB SDL or DDL) and access it in the way that's easiest for you

### Installing
Note - This library is not on PyPI (yet), you will have to install it from source

- Install [Poetry](https://python-poetry.org/)
- Clone the repository
- Run `poetry install` dependencies
- Run `poetry run pre-commit install` to install pre-commit hooks (optional)

Note - You can either run `poetry shell` to activate the virtualenv and run any command or you can run commands within the virtualenv using `poetry run`.

## Using Edgewise
### How it Works
This library first inspects your EdgeDB with a schema query and builds classes and scalars from that with the help of the [attrs](www.attrs.org) library. In formal computer science this is called an Inversion of Control pattern. You can create a new instance of a class by calling `edgewise.new_doc('Object')` where 'Object' is the name of your EdgeDB object. All edgewise classes inherit from `Document` which provides several useful abstractions for you.

### Basic Usage - Objects
Python 3.8 allows for async/await in the repl, which can be activated [thusly](https://docs.python.org/3/using/cmdline.html#id5), as noted on the Python Software Foundation's [Developing with `asyncio`](https://docs.python.org/3/library/asyncio-dev.html) page.
```bash
python -X dev
```
Now you can try out Edgewise. The schema for these examples is available in the [test suite](/tests/).
```python
>>> import edgewise
>>> doc = edgewise.get_doc('Company', {'name':'Fancy Business'})
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
If you'd like to extend a database object, you can do that with the help of some decorators.
**Note:** `@attrs` is required for inheritance to work correctly. To ensure version compatibility import `attrs` from `edgewise`.
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

### Basic Usage - Tuple and Named Tuple
If edgewise encounters a tuple or named tuple scalar in one of your objects, it checks to see if you have a custom definition for that in the scalar registry. This can be accessed with tuple(object, property) as the key.

Schema example:
```

```

```python



```






## EdgeDB Configuration and Connectivity
**WIP**
### Environment Variables

You'll want to configure a user with administrative permissions. For example:

It is generally considered good practice to save database passwords as environmental variables.  

### Extras
#### Timestamping
#### Password Scalar


## Developing with Edgewise
Have a look at [the roadmap](./roadmap.md), which is about as useful as a streetmap of Boston.

### Examples
Examples are available in the examples folder. Some of these will be covered in the tutorial documentation.

If you're considering integrating this library into a framework or project, please consider contributing your changes and/or add an example implementation to the test suite so that breaking changes can be discovered before they mess up your project.

### Dependencies and Tooling
For production code this project notably leverages `attrs` and the EdgeDB python client. You will want to become familiar with how to use and what's underneath `attrs` in order to get the most out of edgewise.
For testing and development, please refer to [pyproject.toml](/pyproject.toml) for more information.

Why DepHell? It's agnostic, feature-rich and lets you choose the formats you want. It could be named better, but that's one the two hardest things in programming [insert meme]. I've had mostly good experiences with Pipenv, though it seems like I might be in the minority there. I've had mostly frustrating experiences with Poetry and again, I think I'm in the minority there as well. If you're considering contributing, I will have an article about my approach to environments and dependency management so you can understand where I'm coming from.

### About the Test Suite
* What's tested and why (to do)
* Using the test suite database to get started (to do)

### Project Utilities
 - [ ] Save your schema, class registrations and scalars in an organized way
 - [ ] See [Projects](projects.md)

### Contributing

Contributions are welcome, please refer to the wiki regarding:
* Opening Issues
* Requesting support

### Versioning
This project ~~uses~~ will use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/agritheory/edgewise/tags).

### Author(s)
* **Tyler Matteson** - *Initial work* - [AgriTheory](https://agritheory.com/)

### License
 This project uses Apache License Version 2.0. See [license.md](./license.md) file for details
