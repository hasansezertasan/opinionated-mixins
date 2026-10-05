# Architecture

opinionated-mixins provides reusable fields for Python storage frameworks. Consumers compose plain mixin classes with their own ORM or ODM base classes.

## Supported frameworks

- SQLAlchemy supplies declarative mixins with columns.
- SQLModel re-exports the SQLAlchemy implementations.
- MongoEngine supplies document field mixins.
- ODMantic supplies annotated field definitions. Its metaclass does not currently collect fields from plain mixin parents; see [issue #39](https://github.com/hasansezertasan/opinionated-mixins/issues/39) and the expected-failure integration tests.

## Layout

`src/opinionated_mixins/contrib/<framework>/` contains one file per mixin. Each framework's `__init__.py` exports its mixins. Shared enums live in `src/opinionated_mixins/enums.py`, and tests mirror the framework layout.

Available mixins cover people, users, announcements, feedback, leads, templates, activity, notifications, timestamps, identifiers, and active flags. Field names and defaults follow the contracts recorded in [the RFC index](docs/rfcs/INDEX.md).

## Design and verification

Mixins remain plain classes so consumers choose the framework base and can combine several mixins. Tests check field definitions, consistency across frameworks, and persistence using SQLite or MongoDB mocks. Optional MongoDB integration tests use testcontainers.

The package has no runtime dependencies. Consumers install their framework; contributors use the development and type-checking groups described in [CONTRIBUTING.md](CONTRIBUTING.md).

New mixins, fields, framework support, and breaking changes require an accepted [RFC](docs/rfcs/README.md). Documentation corrections and examples do not require one.
