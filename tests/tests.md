# Testing Edgewise

Edgewise uses CircleCI.
- [ ] Add instructions for running CircleCI locally

## To Do:
- [X] Test connections
- [ ] Document
- [ ] Precommit hooks for `black` and `isort`
- [ ] Add mypy to testing suite
- [X] Create example data with Mimesis, saving it to the database (integration test)
- [ ] Restore known database with `edgedb restore test_dump -u edgedb --password-from-stdin edgedb -d edgewise`
- [ ] Unit Test `register`
- [ ] Unit Test `register_with_schema`
- [ ] Unit Test `register_scalar`
- [ ] Unit Test `register_scalar_with_schema`
- [ ] Custom Scalar (not in database)
- [ ] Custom Scalar (password)
- [ ] Add Password Scalar to User object
- [ ] Refactor Enum to something useful for User to put it in context
- [ ] Enum
- [ ] Tuple
- [ ] Named Tuple
- [ ] Array
- [X] Add coverage plugin

On hold until JSON refactor
- [ ] Nesting tests
  - [ ] Single existing link, single new link
  - [ ] Multiple new link, multiple existing links
  - [ ] Multiple mixed and existing

## Running the test suite
Test data is generated with [this script](https://gist.github.com/agritheory/8943fd3f4acd5baf65b8b0f8606fa919)


`python -m pytest -s --cov=edgewise`
