# Opinionated Mixins - Analysis Journal

## 2026-02-07: Codebase Analysis & Market Research

### Project Overview

**opinionated-mixins** is an early-stage Python library (v0.0.1) that provides reusable mixin classes for common model patterns across multiple Python ORMs and data frameworks.

### Supported Frameworks (via contrib modules)

- Pydantic (data validation)
- SQLAlchemy (SQL ORM)
- SQLModel (Pydantic + SQLAlchemy)
- MongoEngine (MongoDB ODM)
- ODMantic (MongoDB async ODM)
- WTForms (form validation)
- dataclasses (stdlib)

### Current State

- All contrib modules are **empty** (scaffolded but no implementation)
- Infrastructure is in place: CI (GitHub Actions, Python 3.8-3.12), linting (Ruff), type checking (mypy), testing (pytest)
- Issue templates exist for "Model Proposal" and "Field Proposal"

### Similar Projects

Most existing mixin libraries focus on a **single framework** (usually SQLAlchemy). The unique value proposition of opinionated-mixins is providing **consistent interfaces across multiple ORMs** - an underserved niche.

#### Direct Competitors

| Project                                                                               | Focus                    | Stars | Notes                                                                                                   |
| ------------------------------------------------------------------------------------- | ------------------------ | ----- | ------------------------------------------------------------------------------------------------------- |
| [sqlalchemy-mixins](https://github.com/absent1706/sqlalchemy-mixins)                  | SQLAlchemy only          | ~600  | Most feature-rich - Active Record pattern, Django-like queries, `TimestampsMixin`, nested eager loading |
| [sqlalchemy-easy-softdelete](https://github.com/flipbit03/sqlalchemy-easy-softdelete) | SQLAlchemy only          | ~100  | Single-purpose - adds soft delete with automatic query rewriting                                        |
| [sqlalchemy-soft-delete](https://github.com/miguelgrinberg/sqlalchemy-soft-delete)    | Flask/SQLAlchemy         | ~50   | Miguel Grinberg's implementation                                                                        |
| [dataclass-sqlalchemy-mixins](https://pypi.org/project/dataclass-sqlalchemy-mixins/)  | SQLAlchemy + dataclasses | -     | Combines Python dataclasses with SQLAlchemy                                                             |

#### Related Libraries (Not Pure Mixin Libraries)

| Project                                    | Description                                                                                                                          |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| [SQLModel](https://sqlmodel.tiangolo.com/) | Combines Pydantic + SQLAlchemy in one model definition                                                                               |
| [Ormar](https://collerek.github.io/ormar/) | Async ORM with Pydantic integration, has [pydantic_mixin](https://collerek.github.io/ormar/latest/api/models/mixins/pydantic_mixin/) |
| [Beanie](https://beanie-odm.dev/)          | MongoDB async ODM built on Pydantic                                                                                                  |

### Gap in the Market

None of the existing libraries provide:

- **Cross-framework consistency** (same mixin interface for SQLAlchemy, MongoEngine, Pydantic, etc.)
- **Framework-agnostic design** with contrib modules for each ORM
- **Unified patterns** that work identically whether you're using SQL or NoSQL

#### Example of What opinionated-mixins Could Provide

```python
# SQLAlchemy
from opinionated_mixins.contrib.sqlalchemy import TimestampMixin
class User(Base, TimestampMixin): ...

# MongoEngine
from opinionated_mixins.contrib.mongoengine import TimestampMixin
class User(Document, TimestampMixin): ...

# Pydantic
from opinionated_mixins.contrib.pydantic import TimestampMixin
class User(BaseModel, TimestampMixin): ...

# All three have identical: created_at, updated_at fields
```

This **consistent API across frameworks** is the differentiator.

### Sources

- [sqlalchemy-mixins on PyPI](https://pypi.org/project/sqlalchemy-mixins/)
- [sqlalchemy-mixins on GitHub](https://github.com/absent1706/sqlalchemy-mixins)
- [sqlalchemy-easy-softdelete on PyPI](https://pypi.org/project/sqlalchemy-easy-softdelete/)
- [Reusable SQLModel Mixins (Blog)](https://davidmuraya.com/blog/reusable-sqlmodel-mixins/)
- [Pydantic Mixin Discussions](https://github.com/pydantic/pydantic/discussions/5974)
- [Ormar pydantic_mixin](https://collerek.github.io/ormar/latest/api/models/mixins/pydantic_mixin/)

### Open Questions

- Which mixins to implement first? (Timestamps, SoftDelete, UUID PK are common starting points)
- Should there be a shared protocol/interface that all contrib implementations must satisfy?
- How to handle framework-specific features that don't translate across all ORMs?
