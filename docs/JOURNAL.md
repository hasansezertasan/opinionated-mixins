# Opinionated Mixins - Analysis Journal

## 2026-02-07: Codebase Analysis & Market Research

### Project Overview

**opinionated-mixins** is an early-stage Python library (v0.0.1) that provides reusable mixin classes for common model patterns across multiple Python ORMs and data frameworks.

### Supported Frameworks (storage-layer only, via contrib modules)

- SQLAlchemy (SQL ORM)
- SQLModel (Pydantic + SQLAlchemy, re-exports SQLAlchemy)
- MongoEngine (MongoDB ODM)
- ODMantic (MongoDB async ODM)

### Current State

- All contrib modules are **empty** (scaffolded but no implementation)
- Infrastructure is in place: CI (GitHub Actions, Python 3.10-3.14), linting (Ruff), type checking (mypy), testing (pytest)
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

## 2026-10-09: Declutter Repo Root

### Motivation

The repo root had 34 entries, most of them shared tool configs, which buried the files a
visitor actually looks for. Goal: root holds only things a tool hard-requires there or a
human looks for first.

### What moved and why each landed where it did

- `mise.toml` -> `.config/mise.toml`: mise auto-discovers `.config/mise.toml` and still
  treats the repo as project root. No rewiring needed.
- `.taplo.toml` -> `.config/.taplo.toml`: taplo does not search `.config/`; the tox
  `style` env now passes `--config` explicitly (it also cannot fold the settings into
  pyproject's `[tool.taplo]`).
- `.editorconfig-checker.json` -> `.config/.editorconfig-checker.json`: `ec` does not
  search `.config/`; both callers now pass `-config` explicitly (the prek hook *and* the
  bare `ec` command in the tox `style` env — the second call site is easy to miss).
- `.markdownlint-cli2.jsonc` -> `.config/.markdownlint-cli2.jsonc`: markdownlint-cli2
  does not search `.config/`; the prek hook now passes `--config`. The `extends` path
  inside the config resolved relative to the config file's own directory and needed a
  `../` prefix.
- `.secrets.baseline` -> `.config/.secrets.baseline`: detect-secrets does not auto-discover
  its baseline; the prek hook and the documented scan/audit commands now pass `--baseline`.
- `JOURNAL.md` -> `docs/JOURNAL.md`: narrative notes, no tooling reads it.

Kept at root: `pyproject.toml`, `uv.lock`, `.python-version`, `prek.toml`, `.editorconfig`,
`cobo.lock`, `.copier-answers.yml`, `.gitignore`, `.gitattributes`, `.git_archival.txt`,
`.dockerignore`, `.env.example`, `CITATION.cff`, `LICENSE`, `README.md`, `AGENTS.md`,
`CONTRIBUTING.md` — packaging files, hook runners, VCS attributes and visitor-facing docs
are all anchored to the root by their tools or conventions, and the moving cost exceeds the
benefit.

### Outcome

Root entry count: 34 -> 28. Every moved config was proven resolved, not merely passing:
a wrong config path hard-errors for taplo/ec/detect-secrets, and the markdownlint rules
(MD003/MD004, defined only in the extends chain) fire on a probe file — none of these
silent-fallback paths can hide a missing config.
