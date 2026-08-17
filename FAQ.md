# Frequently Asked Questions (FAQ)

This document addresses common questions and issues related to the opinionated-mixins project.

## General Questions

### What is opinionated-mixins?

opinionated-mixins is a Python library that provides reusable mixins for various frameworks, allowing developers to easily add common functionality to their models without duplicating code.

### Which frameworks are supported?

The project currently supports:

- Pydantic
- SQLAlchemy
- MongoEngine
- ODMantic
- Beanie
- Tortoise
- WTForms
- Dataclasses

### How do I install opinionated-mixins?

You can install the package using pip:

```bash
pip install opinionated-mixins
```

## Usage Questions

### How do I use a mixin in my project?

Each mixin is designed to be easily integrated into your existing models. For example, to use the `PersonMixin` with SQLAlchemy:

```python
from opinionated_mixins.contrib.sqlalchemy.person import Person as SQLAPerson
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base, SQLAPerson):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    email = Column(String(64), index=True, unique=True)
```

### Can I create my own mixins?

Yes, you can create your own mixins by following the same pattern as the existing ones. Ensure they are well-documented and tested.

## Technical Questions

### How do I contribute to the project?

Please refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute.

### How do I report a bug?

If you encounter a bug, please create an issue using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

### How do I request a new feature?

To request a new feature, please create an issue using the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

## Troubleshooting

### I'm having issues with inheritance in ODMantic. What should I do?

ODMantic currently has limitations with inheritance. Please refer to the [ODMantic documentation](https://art049.github.io/odmantic/) for more information and workarounds.

### How do I run the tests?

You can run the tests using pytest:

```bash
uv run pytest
```

## Additional Resources

- [Documentation](https://github.com/hasansezertasan/opinionated-mixins#readme)
- [Issue Tracker](https://github.com/hasansezertasan/opinionated-mixins/issues)
- [Contributing Guidelines](CONTRIBUTING.md)
