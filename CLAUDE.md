# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development

This project uses **Hatch** as its build system and environment manager.

```bash
# Install hatch
pip install --upgrade hatch

# Run tests
hatch run test

# Run a single test file
hatch run test tests/test_something.py

# Run a single test by name
hatch run test -k "test_name"

# Run tests with coverage
hatch run cov

# Lint & format (check only)
hatch fmt --check

# Lint & format (auto-fix)
hatch fmt

# Type checking
hatch run types:typing

# Ruff lint only
hatch run types:style

# Ruff format only
hatch run types:format

# Pre-commit hooks
hatch run pre
```

## Philosophy

This project ships **consensus-based defaults**. Field names, enum values, and behaviors are chosen by researching what popular platforms and frameworks do (GitHub, Zendesk, JIRA, Django, etc.), then picking the most common convention. When adding new mixins or fields, **research first, implement second** — proposals require at least 3 real-world references.

## Architecture

**opinionated-mixins** provides reusable mixin classes for common model patterns (timestamps, UUIDs, soft-delete, etc.) with consistent interfaces across multiple Python ORMs and data frameworks.

### Source Layout

```
src/opinionated_mixins/
├── __init__.py          # Package root
├── __about__.py         # Version (single source of truth for hatch)
├── enums.py             # Shared enums used across all contrib modules
└── contrib/             # Framework-specific implementations
    ├── pydantic/        # Pydantic BaseModel mixins
    ├── sqlalchemy/      # SQLAlchemy declarative mixins
    ├── sqlmodel/        # SQLModel mixins (re-exports from sqlalchemy)
    ├── mongoengine/     # MongoEngine Document mixins
    ├── odmantic/        # ODMantic Model mixins
    ├── wtforms/         # WTForms mixins
    └── dataclasses/     # stdlib dataclass mixins
```

### Key Design Principles

- Each contrib module implements the **same set of mixins** with identical field names and behavior, adapted to its framework's idioms.
- **SQLModel re-exports SQLAlchemy** — `contrib/sqlmodel/` simply re-exports from `contrib/sqlalchemy/` rather than duplicating implementations.
- **Shared enums** live in `src/opinionated_mixins/enums.py`, not inside contrib modules. All frameworks import from there.

### Framework Idiom Patterns

Each framework expresses the same fields differently:

- **SQLAlchemy**: `Column(String(255), nullable=False, index=True)`, uses `@declarative_mixin` and `__abstract__ = True`
- **Pydantic**: `Field(..., min_length=1, max_length=255)` on `BaseModel`
- **MongoEngine**: `StringField(required=True, max_length=255)` with `choices` for enums, uses `.value` for enum defaults
- **ODMantic**: `Field(...)` similar to Pydantic syntax
- **WTForms**: `StringField(label="...", validators=[...])` with `SelectField` for enums, uses `.value` for defaults/choices
- **dataclasses**: `Annotated[str, Doc("...")]` with `dataclasses.field(default=...)`

### Contributing New Mixins

When adding a mixin:

1. Research field names and enum values against real-world platforms (minimum 3 references)
2. Add shared enums to `src/opinionated_mixins/enums.py`
3. Implement in all applicable contrib modules with consistent field names
4. Each mixin gets its own file per framework (e.g., `contrib/sqlalchemy/announcement.py`) and is re-exported from that framework's `__init__.py`
5. For SQLModel, re-export the SQLAlchemy implementation
6. Tests mirror the contrib structure: `tests/<framework>/test_<mixin>.py`
7. Use issue templates "Model Proposal" (for new mixin classes) and "Field Proposal" (for new fields on existing mixins)

## Code Style

- **Python target**: 3.8+ (no walrus operator, no `type` statement, use `typing` imports)
- **Formatter/Linter**: Ruff (Black-compatible formatting, double quotes, spaces)
- **Type checking**: mypy in strict mode
- **Docstring convention**: Google style
- **No runtime dependencies** — the base package has zero deps; frameworks are dev/optional dependencies
