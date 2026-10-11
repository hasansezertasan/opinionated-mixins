---
rfc: "0015"
title: Typed SQLAlchemy Mixin Fields
type: framework
status: proposed
created: 2026-10-11
updated: 2026-10-11
author: hasansezertasan
github_issue: 165
github_pr: null
supersedes: null
superseded_by: null
---

# RFC-0015: Typed SQLAlchemy Mixin Fields

## Summary

Each SQLAlchemy mixin keeps its runtime `Column(...)` declarations and also
declares a `Mapped[...]` annotation for every field inside an
`if TYPE_CHECKING:` block. Type checkers see `instance.username` as `str` and
`instance.email` as `str | None` instead of `Column[str]`. Runtime behavior,
table schemas, and the SQLModel re-export do not change.

This is a `framework` RFC because it changes how one adapter expresses its
mixins. It adds and renames no fields.

## Motivation

The SQLAlchemy mixins declare fields with old-style `Column(...)` assignments.
SQLAlchemy 2.0's typing treats an unannotated `Column[T]` class attribute as a
`Column[T]` on instances too, so consumer code is mistyped:

```python
user: MyUser = session.get(MyUser, 1)
name: str = user.username  # mypy: incompatible type "Column[str]"
```

Consumers have to `cast`, add `# type: ignore`, or redeclare every field. That
defeats the purpose of a shared mixin. SQLAlchemy 2.0's
`Mapped[...]` annotations type these attributes correctly.

Issue #165 records the obstacle. SQLModel composes these same classes through
a re-export, and a mixin that carries `Mapped[...]` annotations at runtime fails
when composed with `SQLModel, table=True`:

```text
PydanticSchemaGenerationError: Unable to generate pydantic-core schema for
sqlalchemy.orm.base.Mapped[str].
```

SQLModel hands every class annotation to Pydantic, and Pydantic cannot build a
schema for `Mapped[str]`. This RFC decides how to get correct types without
breaking that composition.

## Research

This RFC makes no field-naming or enum-value decision, so the
three-reference rule does not apply. It instead records what each typing
mechanism does, verified against SQLAlchemy 2.0.54, SQLModel 0.0.48, and
Pydantic 2.14.0.

| Mechanism | SQLAlchemy runtime | SQLModel `table=True` | Instance type seen by checkers |
| --------- | ------------------ | --------------------- | ------------------------------ |
| `x = Column(String)` (current) | works | builds the table | `Column[str]` |
| `x: Mapped[str] = mapped_column(String)` | works | `PydanticSchemaGenerationError` | `str` |
| `x: Mapped[str] = Column(String)` | works | `PydanticSchemaGenerationError` | `str` |
| `if TYPE_CHECKING: x: Mapped[str]` / `else: x = Column(String)` | works | builds the table | `str` |

The last row works because annotations inside `if TYPE_CHECKING:` never run.
They are absent from the class's runtime `__annotations__`, so neither
SQLAlchemy's declarative scan nor Pydantic sees them. At runtime the class is
identical to the current class. Type checkers treat `TYPE_CHECKING` as true
and analyze only the annotation branch.

Checked with the project's type checkers on a consumer model built from the
mixin. mypy (strict) and basedpyright reveal `str` and `str | None`; ty,
pyrefly, and zuban report no errors. Class-level access
(`select(MyUser).where(MyUser.username == "x")`) type-checks because `Mapped`
provides the class-level `InstrumentedAttribute` overload.

### Framework Adoption

Not applicable. This RFC changes an existing adapter and adds no new framework.

## Design

### Fields

Field names, column types, nullability, defaults, and constraints are
unchanged. Each field gains a `Mapped[...]` annotation whose Python type comes
from its column type:

| Column type | Annotation |
| ----------- | ---------- |
| `String(n)`, `Text` | `str` |
| `Boolean` | `bool` |
| `Integer` | `int` |
| `Numeric` | `Decimal` |
| `Date` | `datetime.date` |
| `DateTime` | `datetime.datetime` |
| `Uuid` | `uuid.UUID` |
| `Enum(E)` | `E` |
| `JSON` | `dict[str, Any]`, matching the ODMantic adapter |

A column declared `nullable=True` gets `T | None`. A `nullable=False` column
gets `T`, even if it has a Python-side default, because a loaded row never
holds `None`.

### Reference Implementation

```python
# SQLAlchemy
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped


@declarative_mixin
class User:
    __abstract__ = True

    if TYPE_CHECKING:
        username: Mapped[str]
        hashed_password: Mapped[str]
        email: Mapped[str | None]
        date_email_verified: Mapped[datetime.datetime | None]
    else:
        username = Column(String(255), nullable=False, unique=True)
        hashed_password = Column(String(1024), nullable=False)
        email = Column(String(254), nullable=True, unique=True)
        date_email_verified = Column(DateTime, nullable=True)
```

MongoEngine and ODMantic are unchanged. ODMantic already declares annotated
fields, and MongoEngine has no equivalent typing mechanism.

### Framework Mixin Idioms

The SQLAlchemy idiom becomes "runtime `Column` plus `TYPE_CHECKING`
`Mapped[...]` annotation". New SQLAlchemy mixins must follow it.

Each field is written twice, so the two declarations can drift.
`tests/sqlalchemy/test_mapped_annotations.py` parses every mixin's
`TYPE_CHECKING` block from source and fails when an annotation disagrees with
its `Column` on name, nullability, or Python type.
`docs/examples/sqlalchemy_typed_access.py` is type-checked in the `style`
environment and fails if instance attributes regress to `Column[...]`.

## Alternatives Considered

1. **Migrate to `Mapped[...] = mapped_column(...)` and give SQLModel its own
   adapter of native `Field(...)` mixins** — rejected for now. It doubles the
   maintained SQL code and adds `sqlmodel` as a test dependency. It also changes
   the import-linter layering (`contrib.sqlmodel` would stop depending on
   `contrib.sqlalchemy`), which needs its own architecture decision. It remains
   the path forward if SQLModel support needs more than the re-export. See
   Consequences.
2. **Migrate to `Mapped[...]` and drop or deprecate the SQLModel re-export** —
   rejected. It is a breaking change to the `contrib.sqlmodel` import path,
   made only to avoid a duplicated declaration that the drift test already
   guards.
3. **Keep `Column(...)` and ship a `.pyi` stub per module** — rejected. A
   stub is a second file per mixin that is easier to forget than an adjacent
   `TYPE_CHECKING` block, and the drift test would need to load stubs.
4. **Annotate with `Mapped[...]` but assign `Column(...)` (no
   `TYPE_CHECKING`)** — rejected. The annotation exists at runtime and SQLModel
   fails exactly as with `mapped_column`.
5. **Do nothing; document `cast` / `# type: ignore` for consumers** —
   rejected. It pushes the cost onto every consumer for every field.

## Discussion Summary

Issue #165 asked for an RFC to choose between keeping the shared mixins (for
example by keeping `Column` for compatibility) and giving SQLModel its own
adapter. The maintainer chose the `TYPE_CHECKING` approach because it keeps
the shared mixins and the current layering, and changes nothing at runtime.
Issue #2 (closed) was earlier context about reusable annotated column types.

## Consequences

- SQLAlchemy consumers get correct instance types (`str`, `str | None`,
  enums, `Decimal`, `datetime`, `uuid.UUID`, and so on) without casts.
  Class-level SQL expressions keep working for type checkers.
- No runtime, schema, or migration change. Existing models and Alembic
  autogenerate output are unaffected. No consumer action is needed.
- SQLModel consumers composing the re-exported mixins also get `Mapped[...]`
  types from their type checker. Runtime behavior is unchanged.
- **Pre-existing SQLModel limitation (not changed by this RFC).** When a
  re-exported mixin is composed with `SQLModel, table=True`, the table and
  columns are created, but the mixin's columns are not Pydantic fields. The
  constructor silently drops them (`Model(username="a").username is None`),
  and assigning `instance.username = "a"` raises
  `ValueError: object has no field "username"`. In practice the re-exported
  mixins contribute schema only. Fixing this needs native SQLModel mixins
  (alternative 1) and is out of scope here. It should be tracked as its own
  issue.
- New constraint: every SQLAlchemy mixin field needs both declarations. The
  drift test enforces this.
- Tooling: basedpyright's `reportUninitializedInstanceVariable` is turned off
  for `src/opinionated_mixins/contrib/sqlalchemy` through an execution
  environment, because the annotations deliberately have no initializer that
  the checker can see. The mypy `var-annotated` override for the adapter is
  removed, since mypy now analyzes only the annotated branch.
- Contrib modules updated: all 13 modules in `contrib/sqlalchemy`.
  `contrib/sqlmodel` is unchanged because it re-exports them.

## Implementation Notes

Implemented in the same PR as this RFC.

## References

- Issue #165: <https://github.com/hasansezertasan/opinionated-mixins/issues/165>
- Issue #2: <https://github.com/hasansezertasan/opinionated-mixins/issues/2>
- SQLAlchemy 2.0, ORM declarative mapping with `Mapped`:
  <https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column>
- SQLAlchemy 2.0, mixins and `declared_attr`:
  <https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html>
- PEP 484, `TYPE_CHECKING`:
  <https://peps.python.org/pep-0484/#runtime-or-type-checking>
- SQLModel: <https://sqlmodel.tiangolo.com/>
