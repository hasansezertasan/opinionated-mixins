---
rfc: "0016"
title: Native SQLModel Mixins
type: breaking-change
status: proposed
created: 2026-10-14
updated: 2026-10-14
author: hasansezertasan
github_issue: 167
github_pr: null
supersedes: null
superseded_by: null
---

# RFC-0016: Native SQLModel Mixins

## Summary

Replace the SQLModel adapter's re-exports of the SQLAlchemy mixins with native
SQLModel implementations: plain classes whose annotated attributes are
`sqlmodel.Field(...)` definitions. Field names, types, lengths, nullability,
defaults, and enums stay identical to the existing mixins; only the way they
are declared changes. The import-linter contract is updated so `sqlmodel` is an
independent sibling of `sqlalchemy`, `mongoengine`, and `odmantic`.

## Motivation

Composing a re-exported SQLAlchemy mixin with `SQLModel, table=True` creates the
table and columns, but the mixin's `Column(...)` attributes are not Pydantic
fields:

- the constructor silently drops them (`Model(username="a").username is None`);
- assignment raises `ValueError: object has no field "username"`;
- model validation, `model_dump()`, and generated schemas omit them.

In practice the re-exported mixins contribute schema only, which defeats the
point of using SQLModel. Issue #167 asks for native mixins.

## Research

No new field names or enum values are introduced, so the field-naming research
of RFCs 0001-0014 stands. The mechanism was checked against the published
behavior of the tools involved:

| Source | Finding | Link |
| ------ | ------- | ---- |
| Pydantic v2 | Field collection walks the whole MRO, so annotated attributes on a plain (non-`BaseModel`) mixin become fields of the model | <https://docs.pydantic.dev/latest/concepts/models/> |
| SQLModel | `Field(sa_type=..., sa_column_kwargs=..., unique=..., primary_key=...)` builds a fresh `Column` per table, so one mixin can back many tables | <https://sqlmodel.tiangolo.com/> |
| Prototype (SQLModel 0.0.48, Pydantic 2.14; see below) | A plain class with `Field` attributes, composed with `SQLModel, table=True`, yields real fields and a separate column per table | this RFC |
| Reusable SQLModel mixins (community write-up) | Counter-example: it inherits the mixin from `SQLModel` (`class TimestampMixin(SQLModel)`), which this RFC rejects (alternative 2) | <https://davidmuraya.com/blog/reusable-sqlmodel-mixins/> |

Minimal prototype used to check the mechanism:

```python
class IntegerID:
    id: int | None = Field(default=None, primary_key=True)


class User:
    username: str = Field(max_length=255, unique=True)
    email: str | None = Field(default=None, max_length=254, unique=True)


class A(IntegerID, User, SQLModel, table=True):
    __tablename__ = "a"


class B(IntegerID, User, SQLModel, table=True):
    __tablename__ = "b"


assert A(username="x").username == "x"  # constructor keeps the value
assert A.__table__.c.username.unique and A.__table__.c.username.type.length == 255
assert A.__table__.c.username is not B.__table__.c.username  # one column per table
```

`Field(sa_column=Column(...))` is deliberately avoided: a `Column` instance can
attach to only one `Table`, so sharing it on a mixin breaks the second model.

## Design

### Fields

Unchanged from the SQLAlchemy adapter for every mixin (`CreatedAt`,
`UpdatedAt`, `IsActive`, `IntegerID`, `UUIDID`, `User`, `Person`, `Announcement`,
`Feedback`, `Template`, `Lead`, `Activity`, `Notification`). The mapping from
`Column` arguments to SQLModel is:

| SQLAlchemy | SQLModel |
| ---------- | -------- |
| `String(n)` | `str` + `Field(max_length=n)` |
| `Text` | `str` + `Field(sa_type=Text)` |
| `nullable=True` | `T \| None` with `default=None`, unless the column has a non-`None` default (`Lead.probability` is `int \| None` with `default=0`) |
| `nullable=False` | non-optional `T` |
| `primary_key=True, autoincrement=True` (`IntegerID`) | `int \| None` with `default=None`, so the database generates it and it stays optional in Pydantic |
| `unique=True`, `primary_key=True` | same keywords on `Field` |
| `DateTime(timezone=True)` | `Field(sa_type=DateTime(timezone=True))` |
| `default=lambda: ...` | `Field(default_factory=...)` |
| `onupdate=...` | `Field(sa_column_kwargs={"onupdate": ...})` |
| `Enum(E)` | `E` annotation (SQLModel maps enums) |
| `Numeric(12, 2)` | `Decimal` + `max_digits=12, decimal_places=2` |
| `JSON` | `dict[str, Any]` + `Field(sa_type=JSON)` |
| `doc=...` | `Field(description=..., sa_column_kwargs={"doc": ...})`, so both Pydantic schemas and `Column.doc` keep the text |

### Reference Implementation

```python
# SQLModel
class IsActive:
    is_active: bool = Field(default=True)


class UpdatedAt:
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"onupdate": lambda: datetime.datetime.now(datetime.timezone.utc)},
    )
```

Mixins remain plain classes; they never inherit from `SQLModel`.

## Alternatives Considered

1. **Keep re-exporting SQLAlchemy** — rejected: columns are not Pydantic fields,
   which is the bug reported in #167.
2. **Inherit mixins from `SQLModel`** — rejected: violates the "never inherit
   from a framework base" rule and breaks composition with other bases.
3. **A metaclass that converts `Column` to fields** (as ODMantic does) — rejected:
   SQLModel and Pydantic already collect plain-class annotations, so no
   metaclass is needed.
4. **`Field(sa_column=Column(...))`** — rejected: a `Column` cannot be shared
   across tables.

## Discussion Summary

Issue #167 is the follow-up to #165 (typed `Mapped[...]` fields), whose
annotations made SQLModel users' type checkers believe the fields worked.

## Consequences

- SQLModel mixin fields work in constructors, assignment, validation, and dumps.
- `opinionated_mixins.contrib.sqlmodel.X is opinionated_mixins.contrib.sqlalchemy.X`
  no longer holds. Code relying on that identity, or on `Column` attributes on
  the mixin class (e.g. `Mixin.username.unique`), must use `Model.__table__`.
- Required fields (for example `username`) are required by the Pydantic model
  but, as for any `table=True` SQLModel, are not validated on `__init__`;
  the database `NOT NULL` constraint still applies.
- `sqlmodel` becomes an optional/dev dependency; the base package still has no
  runtime dependencies.
- `pyproject.toml` import-linter layers list `contrib.sqlmodel` as an independent
  sibling layer.

## Implementation Notes

Filled in after merge.

## References

- <https://github.com/hasansezertasan/opinionated-mixins/issues/167>
