# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development

This project uses **uv** for dependency management and **hatchling** as the build backend.

```bash
# Install dependencies
uv sync --group dev --group types

# Run tests
uv run pytest tests

# Run a single test file
uv run pytest tests/test_something.py

# Run a single test by name
uv run pytest -k "test_name"

# Run tests with coverage
uv run coverage run -m pytest tests
uv run coverage combine  # if parallel
uv run coverage report

# Lint (check only)
uv run ruff check .

# Lint (auto-fix)
uv run ruff check --fix .

# Format (check only)
uv run ruff format --check .

# Format (auto-fix)
uv run ruff format .

# Type checking
uv run mypy --install-types --non-interactive src/opinionated_mixins
```

## Philosophy

This project ships **consensus-based defaults**. Field names, enum values, and behaviors are chosen by researching what popular platforms and frameworks do (GitHub, Zendesk, JIRA, Django, etc.), then picking the most common convention. When adding new mixins or fields, **research first, implement second** — proposals require at least 3 real-world references.

## Architecture

**opinionated-mixins** provides reusable mixin classes for common model patterns (timestamps, UUIDs, soft-delete, etc.) with consistent interfaces across Python storage frameworks (ORMs & ODMs).

### Source Layout

```
src/opinionated_mixins/
├── __init__.py          # Package root
├── __about__.py         # Version (single source of truth for hatchling)
├── enums.py             # Shared enums used across all contrib modules
└── contrib/             # Framework-specific implementations
    ├── sqlalchemy/      # SQLAlchemy declarative mixins
    ├── sqlmodel/        # SQLModel mixins (re-exports from sqlalchemy)
    ├── mongoengine/     # MongoEngine Document mixins
    └── odmantic/        # ODMantic Model mixins
```

### What Is a Mixin

A mixin is a plain class that provides fields/methods to other classes through multiple inheritance, **without being a standalone base class**. Rules:

1. **Never inherit from a framework base** — no `class Foo(BaseModel)`, no `class Foo(Document)`. The mixin is a plain `class Foo:`. The consumer picks the base.
2. **Not independently instantiable** — mixins are composed, not used alone: `class MyModel(AnnouncementMixin, BaseModel): pass`.
3. **Composable** — multiple mixins combine freely with any compatible base.

```python
# ✅ Correct — true mixin
class Announcement:
    title: str = Field(..., min_length=1, max_length=255)

# ❌ Wrong — couples to framework base
class Announcement(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
```

This applies to **all** contrib modules. Every mixin class must be a plain class with no parent.

### Key Design Principles

- Each contrib module implements the **same set of mixins** with identical field names and behavior, adapted to its framework's idioms.
- **SQLModel re-exports SQLAlchemy** — `contrib/sqlmodel/` simply re-exports from `contrib/sqlalchemy/` rather than duplicating implementations.
- **Shared enums** live in `src/opinionated_mixins/enums.py`, not inside contrib modules. All frameworks import from there.

### Framework Idiom Patterns

Each framework expresses the same fields differently:

- **SQLAlchemy**: `Column(String(255), nullable=False, index=True)`, uses `@declarative_mixin` and `__abstract__ = True`
- **MongoEngine**: `StringField(required=True, max_length=255)` with `choices` for enums, uses `.value` for enum defaults
- **ODMantic**: `Field(...)` similar to Pydantic syntax

### Contributing New Mixins

When adding a mixin:

1. **Write an RFC first** (see `docs/rfcs/TEMPLATE.md`). This includes the research step — a minimum of 3 real-world references for any field-naming or enum-value decision. Implementation begins only after the RFC is accepted. See `docs/rfcs/README.md` for the full process.
2. Add shared enums to `src/opinionated_mixins/enums.py`
3. Implement in all applicable contrib modules with consistent field names
4. Each mixin gets its own file per framework (e.g., `contrib/sqlalchemy/announcement.py`) and is re-exported from that framework's `__init__.py`
5. For SQLModel, re-export the SQLAlchemy implementation
6. Tests mirror the contrib structure: `tests/<framework>/test_<mixin>.py`
7. The issue templates "Model Proposal" / "Field Proposal" / "Framework Proposal" are the optional low-friction intake for an RFC — see `docs/rfcs/README.md`

## Documentation & Decision Records

This project preserves design rationale in-repo via RFCs, so the "why" behind
every mixin is readable offline — without GitHub access.

- **RFC docs**: `docs/rfcs/` — every mixin, field addition, framework adoption, and breaking change has an RFC documenting research, alternatives considered, and consequences.
- **RFC index**: `docs/rfcs/INDEX.md` — auto-generated table (never hand-edit it).
- **Process**: `docs/rfcs/README.md` — the full guide.

When asked to **add** a new mixin, field, or framework:

1. Read existing RFCs for similar work to understand established patterns.
2. Write the RFC first (`docs/rfcs/TEMPLATE.md`); implementation follows acceptance.

When asked **"why is field X named Y?"** or **"why does mixin Z work this way?"**,
the answer is in the corresponding RFC — read it before explaining, rather than
inventing rationale.

## Code Style

- **Python target**: 3.10+ (can use `X | Y` union syntax, `match` statements, `TypeAlias`)
- **Formatter/Linter**: Ruff (Black-compatible formatting, double quotes, spaces)
- **Type checking**: mypy in strict mode
- **Docstring convention**: Google style
- **No runtime dependencies** — the base package has zero deps; frameworks are dev/optional dependencies
