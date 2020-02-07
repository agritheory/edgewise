# edge|wise

This library is designed to be used as an Active Record style Object Relational Mapper for [edge|DB](https://edgedb.com). A `ClassRegistry` object is built from a combination of edge|DB schema and the `@register` decorator, which allows for merging class definition and database schema, allowing for an intentional mismatch between attributes and/or properties in the database and adding class methods. New instances can be created by calling `edgewise.new_doc('Doctype')`.

## To Do
- [x] Bind to app/ database connection pattern
- [x] Get IOC mechanism and registry working
  - [ ] Mutation-only approach?
  - [ ] ~~Shelve/ persist~~ # Not sure this is required and may add needless complexity
  - [ ] [Password IO](http://www.pythondiary.com/blog/Jan.13,2020/creating-transparently-encrypted-field-django.html)
  - [x] Decorator to register non-edgeDB classes
- [ ] Export schema to `module` folder
- [ ] Use a state machine model to trigger python hooks
  - [ ] Use [transitions](https://github.com/pytransitions/transitions) library for FSM?
  - [ ] Save StatePattern object to DB, load into registry as `state_patterns` in separate registry
  - [ ] Generate state charts/ export to scxml? (not `transitions`)
  - [ ] Default transitions ~~are~~ will be automatic:
    - [ ] Init, Before Insert, After Insert, Before Update, After Update, Before Delete, After Delete
    - [ ] Custom example would be "Before Submit, "After Submit"
    - [ ] Another would be adding an "Approve" step

Further work and examples:

- [ ] Quart, POP and Starlette integrations
- [ ] Load test/ benchmark and optimize
- [ ] GUI (framework.../ VueCLI type thing?)
- [ ] Command line doctype creation?
- [ ] Generate Entity Relation Charts from schema, though this should really be part of an quivalent JS project

## Getting Started
### Prerequisites
This library uses python >3.7 and requires that edgeDB be installed. Follow the [installation instructions](https://edgedb.com/docs/tutorial/install) given in the edgeDB documentation.

This library ~~uses~~ will use asyncio by default and generally defers to it whenever possible.


### edge|DB Configuration and Connectivity

You'll want to configure a user with administrative permissions. For example:

It is generally considered good practice to save database passwords as environmental variables.  


### Installing
```
python -m install edgewise
```
If you've read this far you know that you should use a virtual environment and you should do that however you like. But you should do it. For development this project uses Pipenv until something better comes along, which has probably already happened.

## Developing with edge|wise
### Examples
Examples are available in the examples folder. Some of these ~~are~~ will be covered in the tutorial documentation.

If you're considering integrating this library into a framework or project, please consider contributing so that breaking changes can be discovered before they mess up your project.

## Dependencies and Tooling
For production code this project uses `attrs`, `python-dotenv` and the edgedb python client.
For testing and development: `pipenv`, `black`, `pytest`, `hypothesis`, `coverage` and `httpx`. Please refer to the Pipfile for more information.

## Contributing

Contributions are welcome, please refer to the wiki regarding:
* Opening GitHub issues
* Requesting support

## Versioning
This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/agritheory/edgewise/tags).

## Authors
* **Tyler Matteson** - *Initial work* - [AgriTheory](https://agritheory.com/)

## License
 See the [license.md](license.md) file for details
