# TODO

- What are our criteria for deciding on a contract / agreement / consensus mechanism?
- No `index=True` in SQLAlchemy models, it can be declared with `__table_args__` by the user of the library but document that if a field is recommended to be indexed.
- Future: Re-evaluate input/validation-layer frameworks once a layer-aware field naming strategy is defined (see #34):
  - Form Validation: WTForms, Django Forms
  - Data Validation/Serialization: Pydantic, Marshmallow
  - Data Containers: dataclasses
