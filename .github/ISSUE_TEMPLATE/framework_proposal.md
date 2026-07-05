---
name: Framework Proposal
about: Propose adding support for a new ORM or ODM framework
title: 'Framework Proposal: '
labels: framework-proposal
assignees: ''

---

> **Note**: This issue is for discussion only. Once the proposal has traction,
> the next step is a formal RFC. See the [RFC process](../../docs/rfcs/README.md)
> for details. If you have already done the research and want to skip the issue
> stage, you can [open an RFC PR directly](../../docs/rfcs/TEMPLATE.md).

**Which framework are you proposing?**
Name, PyPI package, and link to documentation.

| Detail | Value |
| ------ | ----- |
| Package name | e.g. `tortoise-orm` |
| PyPI link | e.g. https://pypi.org/project/tortoise-orm/ |
| Docs link | |
| Type | ORM / ODM |
| Database backends | e.g. PostgreSQL, MySQL, SQLite |
| Python version support | e.g. 3.10+ |

**Why should this framework be supported?**
A clear and concise explanation of why this framework belongs in the project. Consider adoption, community size, and use cases not covered by existing contrib modules.

**Ecosystem evidence**
Show that this framework has meaningful adoption. Include at least 3 data points.

| Metric | Value | Link |
| ------ | ----- | ---- |
| GitHub stars | | |
| PyPI monthly downloads | | |
| Last release date | | |
| Other (Stack Overflow tags, Discord members, etc.) | | |

**Mixin implementation idioms**
Describe how mixins would be expressed in this framework. Show a short example of a field definition and a mixin class.

```python
# Example: how does this framework define a string field with max_length, required, and indexed?
```

```python
# Example: how would a mixin class look? (plain class, abstract base, metaclass, etc.)
```

**Key questions**
- Can mixins be plain classes (no framework base), consistent with this project's mixin rules?
- Does the framework support enum fields natively or require a workaround?
- Can it re-export from an existing contrib module (like SQLModel re-exports from SQLAlchemy), or does it need a full implementation?

**Existing contrib modules**
For reference, the project currently supports: SQLAlchemy, SQLModel (re-exports SQLAlchemy), MongoEngine, ODMantic.

**Additional context**
Add any other context, links, or screenshots here.
