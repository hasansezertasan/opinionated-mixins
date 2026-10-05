# Frequently asked questions

## Which frameworks are supported?

SQLAlchemy, SQLModel, MongoEngine, and ODMantic. These are storage frameworks; input validation libraries and form frameworks are outside the current scope. See [ARCHITECTURE.md](ARCHITECTURE.md) for framework limitations.

## How do I install the package?

```sh
pip install opinionated-mixins
```

Install your chosen framework separately. The base package has no runtime dependencies and requires Python 3.10 or newer.

## How do I use a mixin?

Compose it with your application's framework base:

```python
from opinionated_mixins.contrib.sqlalchemy import Person
from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Person, Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
```

`Contact` receives the Person fields, including `first_name`, `last_name`, `phone_number`, `street_address`, and `date_of_birth`. You can override columns on the concrete model.

## Why does ODMantic inheritance fail?

ODMantic's metaclass does not collect annotations from plain mixin parents. This is tracked in [issue #39](https://github.com/hasansezertasan/opinionated-mixins/issues/39). The [Starlette example](examples/starlette_admin_odmantic/README.md) declares fields directly as a workaround.

## How do I run the checks?

```sh
uv sync --group dev --group types
uv run pytest tests
uv run ruff check .
uv run ruff format --check .
uv run mypy src/opinionated_mixins
```

## How do I propose a change or report a bug?

See [CONTRIBUTING.md](CONTRIBUTING.md). New mixins, fields, framework support, and breaking changes follow the [RFC process](docs/rfcs/README.md). For bugs, use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include a minimal reproduction.
