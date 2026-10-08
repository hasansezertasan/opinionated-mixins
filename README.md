# opinionated-mixins

[![CI](https://github.com/hasansezertasan/opinionated-mixins/actions/workflows/test.yml/badge.svg)](https://github.com/hasansezertasan/opinionated-mixins/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![PyPI - Version](https://img.shields.io/pypi/v/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![License](https://img.shields.io/github/license/hasansezertasan/opinionated-mixins.svg)](https://github.com/hasansezertasan/opinionated-mixins/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/opinionated-mixins)](https://github.com/hasansezertasan/opinionated-mixins)

[![Downloads](https://pepy.tech/badge/opinionated-mixins)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Month](https://pepy.tech/badge/opinionated-mixins/month)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Week](https://pepy.tech/badge/opinionated-mixins/week)](https://pepy.tech/project/opinionated-mixins)

Opinionated, consensus-driven model mixins — timestamps, feedback, announcements — consistent across Python storage frameworks (ORMs & ODMs).

## Why?

Most projects need timestamps, soft-delete, announcements, feedback forms — and each time, you re-invent the field names, the enum values, the defaults. Should it be `created_at` or `date_created`? Is the status field called `state` or `status`? Is "resolved" a valid status or should it be "closed"?

**opinionated-mixins** makes these decisions for you, based on what the industry already agreed on.

Think of it like:

- [**Mobbin**](https://mobbin.com/) — instead of designing UI patterns from scratch, you reference what top apps already do
- [**shadcn/ui**](https://ui.shadcn.com/) — copy well-designed components into your project and customize from there
- [**Bootstrap**](https://getbootstrap.com/) — standardized building blocks so teams stop bikeshedding

Same idea, applied to data models. Use the standard way. Change it when you need it.

## How It Works

Every field name, enum value, and default is chosen by researching what popular platforms and frameworks do (GitHub, Zendesk, JIRA, Django packages, etc.), then picking the most common convention. Proposals require [at least 3 real-world references](.github/ISSUE_TEMPLATE/model_proposal.md).

The same mixin is implemented across all supported frameworks with **identical field names and behavior**, adapted to each framework's idioms.

## Related Projects and Inspiration

These adjacent projects helped shape the way this library thinks about shared conventions, schemas, and reusable model contracts:

- [**awesome-json-schema**](https://github.com/zinnia-ai/awesome-json-schema) — a curated collection of JSON Schema resources, tools, and examples
- [**OpenDTO Specification**](https://github.com/dreamscale-io/OpenDTO-Specification) — an open specification for standardized DTO design and interoperability
- [**Schema.org**](https://github.com/schemaorg/schemaorg) — a large, established shared vocabulary project for structured data

### Example

```python
from opinionated_mixins.contrib.sqlalchemy import Announcement


class MyAnnouncement(Base, Announcement):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    # Gets: title (str, indexed), content (text), category (enum)
```

Switch to MongoDB? Same fields, same names:

```python
from opinionated_mixins.contrib.mongoengine import Announcement


class MyAnnouncement(Document, Announcement):
    pass
    # Same: title, content, category — with MongoEngine field types
```

## Supported Frameworks

| Framework       | Type                          | Use Case                      |
| --------------- | ----------------------------- | ----------------------------- |
| **SQLAlchemy**  | SQL ORM                       | Declarative model mixins      |
| **SQLModel**    | SQL ORM (Pydantic + SA)       | Re-exports SQLAlchemy mixins  |
| **MongoEngine** | MongoDB ODM                   | Document field mixins         |
| **ODMantic**    | MongoDB async ODM             | Model field mixins            |

## Available Mixins

| Mixin | Fields | Shared Enums |
| ----- | ------ | ------------ |
| **Announcement** | `title`, `content`, `category` | `AnnouncementCategory` (8 values) |
| **Feedback** | `subject`, `content`, `category`, `status` | `FeedbackCategory` (4), `FeedbackStatus` (4) |
| **Lead** | `title`, `salutation`, `job_title`, `company_name`, `website`, `linkedin_url`, `status`, `source`, `industry`, `rating`, `opportunity_amount`, `currency`, `probability`, `close_date`, `last_contacted`, `next_follow_up`, `description`, `is_active` | `LeadStatus` (5), `LeadSource` (7), `LeadRating` (3) |
| **Person** | `first_name`, `last_name`, `middle_name`, `phone_number`, `email`, `street_address`, `postal_code`, `city`, `country`, `date_of_birth`, `bio` | — |
| **Template** | `name`, `content`, `format`, `type` | `TemplateFormat` (3), `TemplateType` (4) |
| **User** | `username`, `hashed_password`, `email`, `date_email_verified` | — |

See [open proposals](https://github.com/hasansezertasan/opinionated-mixins/issues?q=is%3Aopen+label%3Amodel-proposal) for upcoming mixins.

## Installation

```console
pip install opinionated-mixins
```

Zero runtime dependencies. Framework packages (SQLAlchemy, MongoEngine, etc.) are your responsibility — you already have them in your project.

## Architecture

opinionated-mixins provides reusable fields for Python storage frameworks. Consumers compose plain mixin classes with their own ORM or ODM base classes.

### Framework implementations

- SQLAlchemy supplies declarative mixins with columns.
- SQLModel re-exports the SQLAlchemy implementations.
- MongoEngine supplies document field mixins.
- ODMantic supplies annotated field definitions through a small compatibility metaclass so plain mixin fields become ODMantic model fields when composed with `odmantic.Model`.

### Layout

`src/opinionated_mixins/contrib/<framework>/` contains one file per mixin. Each framework's `__init__.py` exports its mixins. Shared enums live in `src/opinionated_mixins/enums.py`, and tests mirror the framework layout.

Available mixins cover people, users, announcements, feedback, leads, templates, activity, notifications, timestamps, identifiers, and active flags. Field names and defaults follow the contracts recorded in [the RFC index](docs/rfcs/INDEX.md).

### Design and verification

Mixins remain plain classes so consumers choose the framework base and can combine several mixins. Tests check field definitions, consistency across frameworks, and persistence using SQLite or MongoDB mocks. Optional MongoDB integration tests use testcontainers.

The package has no runtime dependencies. Consumers install their framework; contributors install development, test, and style tools with `uv sync`.

New mixins, fields, framework support, and breaking changes require an accepted [RFC](docs/rfcs/README.md). Documentation corrections and examples do not require one.

## Development

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies
uv sync

# Run tests
uv run pytest tests

# Run tests with coverage
uv run coverage run -m pytest tests
uv run coverage report

# Lint (check / auto-fix)
uv run ruff check .
uv run ruff check --fix .

# Format (check / auto-fix)
uv run ruff format --check .
uv run ruff format .

# Type checking
uv run mypy --install-types --non-interactive src/opinionated_mixins
```

## Roadmap

The [RFC index](docs/rfcs/INDEX.md) records accepted designs and the status of proposals. [Open issues](https://github.com/hasansezertasan/opinionated-mixins/issues) track implementation work.

### Priorities

- Expand ODMantic examples now that plain mixin composition is supported.
- Expand working examples and document framework-specific limitations.
- Extend integration coverage for storage behavior and mixin composition.

The library already includes timestamp, active-flag, integer-ID, and UUID-ID mixins. CI runs linting, formatting, type checking, and tests on Python 3.10 and 3.14.

Additional mixins, fields, or storage frameworks require research and an accepted RFC. See [CONTRIBUTING.md](CONTRIBUTING.md) to propose work.

### Proposed additional mixins

The earlier design discussion proposed the following mixins. These are candidates for RFCs; the remaining field names and contracts are provisional.

[Issue #115](https://github.com/hasansezertasan/opinionated-mixins/issues/115) tracks the partial and unimplemented proposals below, along with framework coverage candidates.

| Proposal | Current coverage | Remaining work |
| --- | --- | --- |
| Timestamp | [CreatedAt](docs/rfcs/0001-created-at-mixin.md) and [UpdatedAt](docs/rfcs/0002-updated-at-mixin.md) provide `created_at` and `updated_at`. | Implemented as separate composable mixins. |
| UUID | [UUIDID](docs/rfcs/0005-uuid-id-mixin.md) provides UUID primary keys for SQLAlchemy and SQLModel. | Implemented for SQL storage; MongoDB models use their native identifiers. |
| SoftDelete | [IsActive](docs/rfcs/0003-is-active-mixin.md) provides an active flag. | A dedicated `deleted_at` / `deleted_by` contract. |
| Audit | [Activity](docs/rfcs/0007-activity-mixin.md) records events and their actors. | Record-level `created_by` / `updated_by` fields. |
| Address | [Person](docs/rfcs/0009-person-mixin.md) includes street address, city, postal code, and country. | A dedicated address mixin, including additional address lines and state/province. |
| Contact | Person includes email and phone number; Lead includes website and LinkedIn URL. | A dedicated contact mixin and a decision on mobile/fax fields. |
| Status | Feedback and Lead have domain-specific status enums. | A general status mixin with change reason, time, and actor. |
| Slug | No dedicated implementation. | URL-friendly slug fields and uniqueness rules. |
| Metadata | Activity and Notification include JSON `data`. | A general metadata/tags contract. |
| Version | No dedicated implementation. | Version, latest-version flag, and parent reference. |
| Priority | No dedicated implementation. | Priority and ordering fields. |
| Expiration | No dedicated implementation. | Expiration time and computed expiry behavior. |

### Framework considerations

Each accepted mixin should provide consistent field names and behavior across applicable supported frameworks, using the framework's native field types, constraints, and validation.

- **SQLAlchemy**: supported; declarative columns, types, and constraints.
- **MongoEngine**: supported; document fields and validation.
- **ODMantic**: supported annotated field definitions with plain mixin composition.
- **SQLModel**: supported through re-exports of SQLAlchemy implementations.
- **TortoiseORM**: proposed expansion; native ORM field definitions and persistence tests.
- **Beanie**: proposed expansion; document fields compatible with Pydantic validation, with the consumer choosing the document base.
- **Pydantic**: proposed input-layer expansion; annotated fields and validation, with the consumer choosing the model base.
- **Dataclasses**: proposed expansion; field annotations and defaults.
- **WTForms**: proposed input-layer expansion; form fields and validators.

The last five frameworks are roadmap candidates, not current support. Adding them requires accepted framework RFCs; Pydantic, dataclasses, and WTForms also require revisiting the current storage-only scope.

## Frequently asked questions

### Which frameworks are supported?

SQLAlchemy, SQLModel, MongoEngine, and ODMantic. These are storage frameworks; input validation libraries and form frameworks are outside the current scope. See [Architecture](#architecture) for framework limitations.

### How do I install the package?

```sh
pip install opinionated-mixins
```

Install your chosen framework separately. The base package has no runtime dependencies and requires Python 3.10 or newer.

### How do I use a mixin?

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

### Can ODMantic models inherit fields from these mixins?

Yes. ODMantic mixins use a compatibility metaclass that copies mixin annotations into the concrete model namespace before ODMantic builds the model. The [Starlette example](examples/starlette_admin_odmantic/README.md) still declares fields directly where it intentionally uses `datetime.datetime` for BSON date storage.

### How do I run the checks?

```sh
uv sync
uv run pytest tests
uv run ruff check .
uv run ruff format --check .
uv run mypy src/opinionated_mixins
```

### How do I propose a change or report a bug?

See [CONTRIBUTING.md](CONTRIBUTING.md). New mixins, fields, framework support, and breaking changes follow the [RFC process](docs/rfcs/README.md). For bugs, use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include a minimal reproduction.

## Contributing

New mixin ideas? Open a [Model Proposal](https://github.com/hasansezertasan/opinionated-mixins/issues/new?template=model_proposal.md). New fields on existing mixins? Open a [Field Proposal](https://github.com/hasansezertasan/opinionated-mixins/issues/new?template=field_proposal.md).

Both require real-world references — this project runs on consensus, not opinion.

## License

`opinionated-mixins` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
