# opinionated-mixins

[![CI](https://github.com/hasansezertasan/opinionated-mixins/actions/workflows/test.yml/badge.svg)](https://github.com/hasansezertasan/opinionated-mixins/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![PyPI - Version](https://img.shields.io/pypi/v/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![License](https://img.shields.io/github/license/hasansezertasan/opinionated-mixins.svg)](https://github.com/hasansezertasan/opinionated-mixins/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/opinionated-mixins)](https://github.com/hasansezertasan/opinionated-mixins)

[![Downloads](https://pepy.tech/badge/opinionated-mixins)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Month](https://pepy.tech/badge/opinionated-mixins/month)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Week](https://pepy.tech/badge/opinionated-mixins/week)](https://pepy.tech/project/opinionated-mixins)

Opinionated, consensus-driven model mixins — timestamps, feedback, announcements — consistent across Python ORMs and data frameworks.

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

### Example

```python
from opinionated_mixins.contrib.sqlalchemy import Announcement

class MyAnnouncement(Base, Announcement):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)
    # Gets: title (str, indexed), content (text), category (enum)
```

Switch to Pydantic? Same fields, same names:

```python
from opinionated_mixins.contrib.pydantic import Announcement

class MyAnnouncement(Announcement):
    id: int
    # Same: title, content, category — with Pydantic validation
```

## Supported Frameworks

| Framework       | Type                          | Use Case                      |
| --------------- | ----------------------------- | ----------------------------- |
| **SQLAlchemy**  | SQL ORM                       | Declarative model mixins      |
| **SQLModel**    | SQL ORM (Pydantic + SA)       | Re-exports SQLAlchemy mixins  |
| **Pydantic**    | Data validation               | BaseModel mixins with `Field` |
| **MongoEngine** | MongoDB ODM                   | Document field mixins         |
| **ODMantic**    | MongoDB async ODM             | Model field mixins            |
| **WTForms**     | Form validation               | Form field mixins             |
| **dataclasses** | Standard library              | `@dataclass` field mixins     |

## Available Mixins

| Mixin | Fields | Shared Enum |
| ----- | ------ | ----------- |
| **Announcement** | `title`, `content`, `category` | `AnnouncementCategory` (8 values) |

More coming — see [open proposals](https://github.com/hasansezertasan/opinionated-mixins/issues?q=is%3Aopen+label%3Amodel-proposal).

## Installation

```console
pip install opinionated-mixins
```

Zero runtime dependencies. Framework packages (SQLAlchemy, Pydantic, etc.) are your responsibility — you already have them in your project.

## Contributing

New mixin ideas? Open a [Model Proposal](https://github.com/hasansezertasan/opinionated-mixins/issues/new?template=model_proposal.md). New fields on existing mixins? Open a [Field Proposal](https://github.com/hasansezertasan/opinionated-mixins/issues/new?template=field_proposal.md).

Both require real-world references — this project runs on consensus, not opinion.

## License

`opinionated-mixins` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
