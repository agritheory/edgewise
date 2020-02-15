# Edgewise Roadmap
A brain dump of ideas for this project, good and bad.


## Triage/ Bug Fixes
- [ ] Handle `tuple` and `namedtuple` scalars explicitly
  - Could be referenced as `tuple(object, property)` key in scalar registry
- [x] Handle `enum` scalar as part of scalar registry
- [X] Switch to ~~poetry~~ [DepHell](https://github.com/dephell/dephell)
- [X] Make selectable sync/async interface.
- [ ] Refactor schema queries to run synchronously, use and load a shared edgedb connection class
- [X] Document alternative `python -X dev` which also allows `await`ing in the repl when async API is done
- [ ] Docker >> Tox >> Tests >> GitLabCI config
- [ ] Nested update - is this even a thing?

## To Do/ Roadmap
- [ ] Refactor IO to JSON (start with schema queries)
- [x] Bind to app/ database connection pattern
- [x] Get IOC mechanism and registry working
- [x] Decorator to register non-edgeDB classes to work with `new_doc`
- [x] `@scalar(object, property)` class decorator with pack and unpack methods
- [X] Register scalars in class registry (with schema query)
- [x] Add edgewise.new_scalar API
- [X] ~~Mutation-only approach~~ Private method updates only
- [ ] ~~Shelve/ persist~~ Not sure this is required and may add needless complexity
- [ ] Custom Password scalar [Password IO](http://www.pythondiary.com/blog/Jan.13,2020/creating-transparently-encrypted-field-django.html)
- [ ] Provide esdl utilities for timestamping and user modification

### State Machine/ Trigger Integration

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
- [ ] ~~Command line doctype creation?~~ There's no strong reason to to this, EdgeDB's SDL is better than anything that could be accomplished on the command line. Maybe to create boilerplate edsl and class, helps with app structure
- [ ] Export schema to `module` folder
- [ ] Generate Entity Relation Charts from schema, though this should really be part of an equivalent JS/TS project? `edgewise.js` -> seems worth it to have matching APIs
