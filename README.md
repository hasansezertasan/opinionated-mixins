# opinionated-mixins

[![CI](https://github.com/hasansezertasan/opinionated-mixins/actions/workflows/test.yml/badge.svg)](https://github.com/hasansezertasan/opinionated-mixins/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![PyPI - Version](https://img.shields.io/pypi/v/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![License](https://img.shields.io/github/license/hasansezertasan/opinionated-mixins.svg)](https://github.com/hasansezertasan/opinionated-mixins/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/opinionated-mixins)](https://github.com/hasansezertasan/opinionated-mixins)

[![Downloads](https://pepy.tech/badge/opinionated-mixins)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Month](https://pepy.tech/badge/opinionated-mixins/month)](https://pepy.tech/project/opinionated-mixins)
[![Downloads/Week](https://pepy.tech/badge/opinionated-mixins/week)](https://pepy.tech/project/opinionated-mixins)

Reusable mixin classes for common model patterns across multiple Python ORMs and data frameworks.

## Supported Frameworks

| Framework       | Purpose                       |
| --------------- | ----------------------------- |
| **Pydantic**    | Data validation models        |
| **SQLAlchemy**  | SQL ORM models                |
| **SQLModel**    | Pydantic + SQLAlchemy hybrid  |
| **MongoEngine** | MongoDB ODM                   |
| **ODMantic**    | MongoDB async ODM             |
| **WTForms**     | Form validation               |
| **dataclasses** | Standard library data classes |

## What It Does

opinionated-mixins provides consistent interfaces for common model patterns, so you get the same fields and behavior regardless of which framework you use:

- **Reusable model fields** (timestamps, UUIDs, soft-delete, etc.)
- **Common model patterns** with consistent interfaces across frameworks

### Example

```python
from opinionated_mixins.contrib.sqlalchemy import TimestampMixin, SoftDeleteMixin

class User(Base, TimestampMixin, SoftDeleteMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Automatically gets: created_at, updated_at, deleted_at, is_deleted
```

---

**Table of Contents**

- [opinionated-mixins](#opinionated-mixins)
  - [Supported Frameworks](#supported-frameworks)
  - [What It Does](#what-it-does)
  - [Installation](#installation)
  - [License](#license)

## Installation

```console
pip install opinionated-mixins
```

## License

`opinionated-mixins` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
