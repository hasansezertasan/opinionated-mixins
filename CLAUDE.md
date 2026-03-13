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

## Architecture

**opinionated-mixins** provides reusable mixin classes for common model patterns (timestamps, UUIDs, soft-delete, etc.) with consistent interfaces across multiple Python ORMs and data frameworks.

### Source Layout

```
src/opinionated_mixins/
├── __init__.py          # Package root
├── __about__.py         # Version (single source of truth for hatch)
└── contrib/             # Framework-specific implementations
    ├── pydantic/        # Pydantic BaseModel mixins
    ├── sqlalchemy/      # SQLAlchemy declarative mixins
    ├── sqlmodel/        # SQLModel mixins
    ├── mongoengine/     # MongoEngine Document mixins
    ├── odmantic/        # ODMantic Model mixins
    ├── wtforms/         # WTForms mixins
    └── dataclasses/     # stdlib dataclass mixins
```

### Key Design Principle

Each contrib module implements the **same set of mixins** with identical field names and behavior, adapted to its framework's idioms. For example, a `TimestampMixin` in `contrib/sqlalchemy/` should expose the same `created_at` and `updated_at` fields as its counterpart in `contrib/pydantic/`.

### Contributing New Mixins

When adding a mixin:

1. Implement it in all applicable contrib modules with consistent field names
2. Each contrib module's `__init__.py` is the sole file for that framework's mixins
3. Use issue templates "Model Proposal" (for new mixin classes) and "Field Proposal" (for new fields on existing mixins)

## Code Style

- **Python target**: 3.8+ (no walrus operator, no `type` statement, use `typing` imports)
- **Formatter/Linter**: Ruff (Black-compatible formatting, double quotes, spaces)
- **Type checking**: mypy in strict mode
- **Docstring convention**: Google style
- **No runtime dependencies** — the base package has zero deps; frameworks are dev/optional dependencies
