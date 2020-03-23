# Testing Edgewise

Edgewise is setup up to build and run with the official Docker image from EdgeDB.

## To Do:
- [X] Test connections
- [ ] Document
- [X] Create example data with Mimesis, saving it to the database (integration test)
- [ ] Restore known database with `edgedb restore test_dump -u edgedb --password-from-stdin edgedb -d edgewise-test`
- [ ] Unit Test `register`
- [ ] Unit Test `register_with_schema`
- [ ] Unit Test `register_scalar`
- [ ] Unit Test `register_scalar_with_schema`
- [ ] Custom Scalar (not in database)
- [ ] Custom Scalar (password)
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

`python -m pytest -s --cov=edgewise`
