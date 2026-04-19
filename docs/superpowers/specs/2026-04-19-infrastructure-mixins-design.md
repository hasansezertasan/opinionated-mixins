# Infrastructure Mixins Design

**Issue:** [#8](https://github.com/hasansezertasan/opinionated-mixins/issues/8)
**Date:** 2026-04-19
**Status:** Approved

## Problem

Common model fields like `id`, `created_at`, `updated_at`, and `is_active` are copy-pasted across projects. This project already provides domain mixins (Announcement, User, etc.) but lacks these foundational infrastructure mixins.

## References

- [advanced-alchemy/mixins](https://github.com/litestar-org/advanced-alchemy/tree/main/advanced_alchemy/mixins) — AuditColumns, BigIntPrimaryKey, UUIDPrimaryKey, etc.
- [bixomix](https://github.com/Bixoto/bixomix) — CreatedAtMixin, UpdatedAtMixin, EnabledMixin
- [Django](https://docs.djangoproject.com/en/stable/ref/contrib/auth/) — `is_active` convention on User model

## Scope

Five new granular mixins. No combo/convenience mixins — users compose what they need.

### Mixin Definitions

| Mixin | Frameworks | Field | Type | Default |
|-------|-----------|-------|------|---------|
| `CreatedAt` | SQLAlchemy, SQLModel, MongoEngine, ODMantic | `created_at` | datetime (UTC) | `datetime.now(UTC)` at creation |
| `UpdatedAt` | SQLAlchemy, SQLModel, MongoEngine, ODMantic | `updated_at` | datetime (UTC) | `datetime.now(UTC)` at creation, auto-updates on save |
| `IsActive` | SQLAlchemy, SQLModel, MongoEngine, ODMantic | `is_active` | bool | `True` |
| `IntegerID` | SQLAlchemy, SQLModel | `id` | int | auto-increment primary key |
| `UUIDID` | SQLAlchemy, SQLModel | `id` | UUID | `uuid4()` primary key |

### Design Decisions

1. **Pure granular** — no combo mixins (e.g., no `TimestampMixin`). Users compose: `class Foo(CreatedAt, UpdatedAt, Base)`.
2. **`is_active` not `enabled`** — follows Django/Python convention for boolean fields (`is_*` prefix). Default `True` (most models start active).
3. **ID mixins SQL-only** — MongoEngine/ODMantic auto-generate `_id` (ObjectId). Overriding that fights framework idioms.
4. **App-side defaults** — use `default=` (Python-side) not `server_default=` (DB-side) for portability across frameworks. Exception: SQLAlchemy may use `server_default` where appropriate for DB-level guarantees.
5. **Field names** — `created_at`, `updated_at`, `is_active`, `id`. Matches consensus across Django, Rails, Laravel, advanced-alchemy, bixomix.

## Framework Implementations

### SQLAlchemy

```python
@declarative_mixin
class CreatedAt:
    __abstract__ = True
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

@declarative_mixin
class UpdatedAt:
    __abstract__ = True
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

@declarative_mixin
class IsActive:
    __abstract__ = True
    is_active = Column(Boolean, nullable=False, default=True)

@declarative_mixin
class IntegerID:
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

@declarative_mixin
class UUIDID:
    __abstract__ = True
    id = Column(Uuid, primary_key=True, default=uuid4)
```

### SQLModel

Re-exports from SQLAlchemy (existing pattern):

```python
from opinionated_mixins.contrib.sqlalchemy.created_at import CreatedAt as CreatedAt
from opinionated_mixins.contrib.sqlalchemy.updated_at import UpdatedAt as UpdatedAt
from opinionated_mixins.contrib.sqlalchemy.is_active import IsActive as IsActive
from opinionated_mixins.contrib.sqlalchemy.integer_id import IntegerID as IntegerID
from opinionated_mixins.contrib.sqlalchemy.uuid_id import UUIDID as UUIDID
```

### MongoEngine

```python
class CreatedAt:
    created_at = DateTimeField(required=True, default=lambda: datetime.now(timezone.utc))

class UpdatedAt:
    updated_at = DateTimeField(required=True, default=lambda: datetime.now(timezone.utc))

class IsActive:
    is_active = BooleanField(required=True, default=True)
```

No ID mixins — MongoEngine handles `_id` natively.

### ODMantic

```python
class CreatedAt:
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UpdatedAt:
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class IsActive:
    is_active: bool = Field(default=True)
```

No ID mixins — ODMantic handles `id` natively via MongoDB ObjectId.

## File Structure

```
src/opinionated_mixins/contrib/
├── sqlalchemy/
│   ├── created_at.py
│   ├── updated_at.py
│   ├── is_active.py
│   ├── integer_id.py
│   ├── uuid_id.py
│   └── __init__.py          # updated with new exports
├── sqlmodel/
│   └── __init__.py          # updated with new re-exports
├── mongoengine/
│   ├── created_at.py
│   ├── updated_at.py
│   ├── is_active.py
│   └── __init__.py          # updated with new exports
└── odmantic/
    ├── created_at.py
    ├── updated_at.py
    ├── is_active.py
    └── __init__.py          # updated with new exports
```

## Tests

```
tests/
├── sqlalchemy/
│   ├── test_created_at.py
│   ├── test_updated_at.py
│   ├── test_is_active.py
│   ├── test_integer_id.py
│   └── test_uuid_id.py
├── sqlmodel/
│   ├── test_created_at.py
│   ├── test_updated_at.py
│   ├── test_is_active.py
│   ├── test_integer_id.py
│   └── test_uuid_id.py
├── mongoengine/
│   ├── test_created_at.py
│   ├── test_updated_at.py
│   └── test_is_active.py
├── odmantic/
│   ├── test_created_at.py
│   ├── test_updated_at.py
│   └── test_is_active.py
└── test_cross_framework_consistency.py  # updated
```

## Open Questions

None. All decisions resolved during brainstorming.
