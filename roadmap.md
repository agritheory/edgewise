# Edgewise Roadmap
A brain dump of ideas for this project, good and bad.


## Short Term Issues
- [ ] Make onboarding simpler (`pip install` and/or Docker)
- [ ] Run `mypy` locally or as part of GitLab Runner, include `mypy` as part of test suite
- [ ] Precommit hook for `black`
- [ ] GitLab Runner local setup instructions
- [ ] Integration test
- [ ] Handle `tuple`, `namedtuple` and `array` scalars explicitly in scalar registry
  - Could be referenced with `tuple(object, property)` key
- [x] Handle `enum` scalar as part of scalar registry
- [ ] Switch from pipenv to ~~poetry~~ ~~[DepHell](https://github.com/dephell/dephell)~~ pip
- [X] Make selectable sync/async interface.
- [X] Refactor schema queries to run synchronously, use and load a shared edgedb connection class
- [X] Document alternative `python -X dev` which also allows `await`ing in the repl when async API is done
- [ ] Docker >> Tox (3.6, 3.7, 3.8) >> Tests >> GitLabCI config
- [ ] Refactor IO to JSON (start with schema queries)
- [ ] Add [async pooled connection](https://edgedb.com/docs/clients/00_python/api/asyncio_con#connection-pools) option
- [ ] Custom Password scalar [Password IO](http://www.pythondiary.com/blog/Jan.13,2020/creating-transparently-encrypted-field-django.html) - include in test suite

## Roadmap
- [x] Bind to app/ database connection pattern
- [x] Get IOC mechanism and registry working
- [x] Decorator to register non-edgeDB classes to work with `new_doc`
- [x] `@scalar(object, property)` class decorator with pack and unpack methods
- [X] Register scalars in class registry (with schema query)
- [x] Add edgewise.new_scalar API
- [ ] Read distinct constraints from schema to setup default primary key - save as __distinct__ property (set)? - use for getting get_doc to
- [X] ~~Mutation-only approach~~ Private method updates only
- [ ] Provide esdl utilities for timestamping and user modification - use inheritance of timestamped object

### State Machine/ Trigger Integration
- [ ] Add state machine for DB queries
- [ ] Use a state machine model to trigger python hooks
  - [ ] Use [transitions](https://github.com/pytransitions/transitions) library for FSM?
  - [ ] Save StatePattern object to DB, load into registry as `state_patterns` in separate registry
  - [ ] Generate state charts/ export to scxml? (not `transitions`)
  - [ ] Default transitions ~~are~~ will be automatic:
    - [ ] Init, Before Insert, After Insert, Before Update, After Update, Before Delete, After Delete
    - [ ] Custom example would be "Before Submit, "After Submit"
    - [ ] Another would be adding an "Approve" step

Further work and examples:

- [ ] Quart, POP and Starlette examples
- [ ] Load test/ benchmark and optimize
- [ ] GUI (framework.../ VueCLI type thing?)
- [ ] ~~Command line doctype creation?~~ There's no strong reason to to this, EdgeDB's SDL is better than anything that could be accomplished on the command line. Maybe to create boilerplate edsl and class, helps with app structure
- [ ] Export schema to `module` folder
- [ ] Generate Entity Relation Charts from schema, though this should really be part of an equivalent JS/TS project? `edgewise.js` -> seems worth it to have matching APIs
