---
rfc: "0014"
title: Slug
type: mixin
status: proposed
created: 2026-10-09
updated: 2026-10-09
author: hasansezertasan
github_issue: 115
github_pr: null
supersedes: null
superseded_by: null
---

# RFC-0014: Slug

## Summary

A `Slug` mixin providing a single required `slug` string of at most 255
characters:
the URL-friendly, human-readable identifier for a record. The mixin defines the
storage contract only. Slug generation, normalization, uniqueness scope, and
slug history remain application concerns, documented with recommendations
rather than baked into the column.

## Motivation

Content-like records (articles, pages, products, categories, tags) are
addressed in URLs by a readable identifier such as `/blog/hello-world` instead
of a numeric or UUID key. Every major web framework and CMS has a field for
this, and they almost all call it `slug`. Projects nevertheless re-declare it
by hand with diverging lengths (Django's default of 50 is a frequent source of
truncation bugs), so a shared contract is useful.

The original design discussion listed `Slug` with candidate fields `slug` and
`title`. Issue #115 tracks it as an unimplemented proposal and asks this RFC to
decide generation/normalization, uniqueness, and indexing rules.

## Research

### Field Naming

| Source | Field name | Length | Unique by default | Generated from | Link |
| ------ | ---------- | ------ | ----------------- | -------------- | ---- |
| Django `SlugField` | `slug` (convention) | 50 | No (opt-in); indexed by default (`db_index=True`) | `title` via admin `prepopulated_fields` | https://docs.djangoproject.com/en/stable/ref/models/fields/#slugfield |
| Wagtail `Page` | `slug` | 255 | Among siblings, enforced in code | `title` when blank | https://docs.wagtail.org/en/stable/reference/pages/model_reference.html |
| WordPress | `post_name` (REST: `slug`) | 200 | Per post type / per parent, enforced in code | `title` | https://developer.wordpress.org/rest-api/reference/posts/ |
| Rails `friendly_id` | `slug` | — | Unique index recommended; UUID suffix on collision | `title` / `name` | https://norman.github.io/friendly_id/file.Guide.html |
| Laravel `spatie/laravel-sluggable` | `slug` | configurable | Yes, `-1`/`-2` suffix; scope configurable | `title` | https://github.com/spatie/laravel-sluggable |
| Strapi `uid` | any attribute of type `uid` | configurable | Generated values are unique; DB `column.unique` is opt-in | `targetField` | https://docs.strapi.io/cms/backend-customization/models |
| Shopify `Product` | `handle` | — | Per shop | `title` | https://shopify.dev/docs/api/admin-graphql/latest/objects/Product |

**Chosen name.** `slug`. It is the field name in Django, Wagtail, friendly_id,
spatie/laravel-sluggable, and the WordPress REST API. Shopify's `handle` and
WordPress's internal `post_name` are outliers.

**Chosen length.** 255, matching Wagtail and this library's other short string
fields (`Template.name`, `User.username`, `Announcement.title`). Django's 50 is
widely overridden, and WordPress's 200 is an implementation detail of its
schema.

**Observed consensus on behavior:**

- **Uniqueness is nearly always wanted, but its scope varies.** WordPress
  scopes it per post type and per parent. Wagtail scopes it among sibling pages.
  spatie/laravel-sluggable supports scoped uniqueness. Multi-tenant and
  localized sites scope it per tenant or locale. friendly_id recommends a plain
  global unique index, and Django leaves uniqueness opt-in.
- **Slugs are looked up by value, so they are indexed.** Django indexes
  `SlugField` by default, and friendly_id recommends a unique index. Since a
  unique index also serves lookups, a separate non-unique index is rarely
  needed.
- **Generate once, do not regenerate.** Django's admin skips saved objects,
  friendly_id 5+ generates only when the slug is `nil`, and Shopify keeps the
  handle after a title change. spatie/laravel-sluggable regenerates by default
  but documents an opt-out. Changing slugs breaks URLs, so the libraries that do
  support it add a history or redirect layer (friendly_id `History`, Spatie
  self-healing URLs, Wagtail's `page_slug_changed` signal).
- **Generators produce lowercase ASCII with hyphens; validators are looser.**
  Django's `slugify()` and `python-slugify` lowercase, use `-` as the separator,
  and default to ASCII. Validators accept more: Django's `validate_slug` allows
  `[-a-zA-Z0-9_]` (Unicode opt-in), Strapi allows `[A-Za-z0-9-_.~]`, and
  Wagtail enables Unicode slugs.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `slug` | `str` | yes | — | at most 255 characters; non-empty in MongoEngine and ODMantic; not unique by default (see below) |

**Generation and normalization.** Out of scope. Most surveyed systems do
generate slugs (Wagtail, WordPress, Shopify, friendly_id, spatie, Strapi), but
each makes different choices: which source field, which slugify function,
whether Unicode is allowed, and how collisions are suffixed (none, `-1`/`-2`,
or a UUID). Generating from a source field would also need framework-specific
hooks (SQLAlchemy events, MongoEngine `clean`, a Pydantic validator) and a
slugify dependency, which this dependency-free package avoids. Consumers set
`slug` explicitly, typically with `django.utils.text.slugify`,
`python-slugify`, or an equivalent, once at creation.

**Format validation.** None beyond length, matching every existing mixin in
this library, none of which validates string format. An ASCII pattern would
reject Unicode slugs (Wagtail, localized sites), and the surveyed validators
disagree on the allowed characters. Each adapter's docstring recommends
slugs that fully match `[a-z0-9]+(?:-[a-z0-9]+)*` (check with `re.fullmatch`;
`re.match` with `$` would accept a trailing newline).

**Minimum length.** MongoEngine and ODMantic reject an empty slug with
`min_length=1`. MongoEngine's `required=True` alone does not reject `""`. The
SQLAlchemy column is `NOT NULL` but, like `Template.name` and `User.username`,
does not reject `""` at the database level. A mixin-level `CheckConstraint`
would collide with the consumer's own `__table_args__`. Consumers that need
the guarantee on SQL add it themselves. Note that slugifying text with no ASCII
letters or digits (for example `slugify("日本語")`) returns `""`.

**Uniqueness and indexing.** The field is not declared `unique` in any
adapter, although all three could declare it (SQLAlchemy `unique=True`,
MongoEngine `unique=True`, ODMantic `Field(unique=True)`). Because the correct
scope varies (global, per parent, per type, per tenant, per locale), a global
unique constraint in the mixin would block valid scoped designs, and dropping
it would require overriding the field. Each adapter's docstring recommends
the index to add instead. This follows #130's SQLAlchemy convention and
extends it to the document adapters:

- a unique index on `slug` when slugs are globally unique, or
- a compound unique index such as `(parent_id, slug)` or `(tenant_id, slug)`
  for scoped slugs.

Caveats the docstrings point out:

- In SQL, a compound unique constraint does not treat `NULL`s as equal, so two
  root rows `(NULL, "about")` are both accepted. Use a partial unique index on
  `slug` where `parent_id IS NULL`, or a non-null root reference. MongoDB
  compound unique indexes do reject them.
- MongoEngine adds `_cls` to indexes on inheritable documents, so the index
  needs `"cls": False` to make `slug` unique across the collection.
- Uniqueness follows the database collation. MySQL's default collations treat
  `Hello` and `hello` as equal; PostgreSQL, SQLite, and MongoDB do not.
  Lowercase slugs avoid the difference.
- A soft-deleted or inactive row keeps its slug reserved unless the unique
  index is partial (for example `WHERE is_active`).

**Slug history.** Out of scope. Old-slug redirect tables are a separate
relational concern and could be proposed as their own RFC.

### Reference Implementation

```python
# SQLAlchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_mixin

__all__ = ["Slug"]


@declarative_mixin
class Slug:
    """Slug mixin for SQLAlchemy models.

    The mixin does not generate or normalize slugs; set ``slug`` explicitly,
    for example with ``slugify(title)`` at creation. Recommended format: fully
    matches ``[a-z0-9]+(?:-[a-z0-9]+)*``. The column does not reject ``""``.

    Indexing recommendations:
    - ``slug``: unique index recommended when slugs are globally unique, or a
      composite unique constraint for scoped slugs (for example per parent or
      per tenant). Composite constraints treat ``NULL`` parents as distinct.

    Example:
        .. code-block:: python

            from sqlalchemy import Index


            class Article(Slug, Base):
                __tablename__ = "articles"
                id = Column(Integer, primary_key=True)

                __table_args__ = (Index("ix_articles_slug", "slug", unique=True),)
    """

    __abstract__ = True

    slug = Column(String(255), nullable=False)
```

```python
# MongoEngine
from typing import Any, ClassVar

from mongoengine import StringField

__all__ = ["Slug"]


class Slug:
    """Slug mixin for MongoEngine documents.

    The mixin does not generate or normalize slugs; set ``slug`` explicitly.
    Recommended format: fully matches ``[a-z0-9]+(?:-[a-z0-9]+)*``.

    Indexing recommendations:
    - ``slug``: add ``{"fields": ["slug"], "unique": True, "cls": False}`` to
      ``meta["indexes"]`` for globally unique slugs (without ``"cls": False``
      MongoEngine indexes ``(_cls, slug)``), or a compound unique index for
      scoped slugs.
    """

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    slug = StringField(required=True, min_length=1, max_length=255)
```

```python
# ODMantic
from odmantic import Field

from ._base import ODManticMixinMetaclass

__all__ = ["Slug"]


class Slug(metaclass=ODManticMixinMetaclass):
    """Slug mixin for ODMantic models.

    The mixin does not generate or normalize slugs; set ``slug`` explicitly.
    Recommended format: fully matches ``[a-z0-9]+(?:-[a-z0-9]+)*``.

    Indexing recommendations:
    - ``slug``: declare ``Index(Model.slug, unique=True)`` in
      ``model_config["indexes"]`` for globally unique slugs, or a compound
      ``Index`` for scoped slugs; ``engine.configure_database`` creates them.
    """

    slug: str = Field(..., min_length=1, max_length=255)
```

SQLModel re-exports the SQLAlchemy implementation.

## Alternatives Considered

1. **`handle` (Shopify) or `post_name` (WordPress)**: rejected. They are
   outliers, and even WordPress exposes `slug` publicly.
2. **Include a `title` field**: rejected. Announcement, Notification, and Lead
   already define `title`, so composing `Slug` with them would declare the
   field twice. The slug's source is also often `name` (friendly_id), so the
   source field belongs to the domain mixin, not to `Slug`.
3. **Global `unique=True` on the field (like `User.username`)**: rejected
   because uniqueness scope varies (WordPress, Wagtail, multi-tenant, i18n), and
   a field-level constraint cannot be narrowed without overriding the field.
4. **Auto-generate from a source field on insert**: rejected. It needs
   framework-specific hooks (SQLAlchemy `before_insert`, MongoEngine `clean`, a
   Pydantic validator), a slugify dependency, and a collision strategy, and
   the surveyed systems disagree on all three.
5. **Format validation (MongoEngine `regex=`, a Pydantic pattern, SQLAlchemy
   `@validates`)**: rejected. No existing mixin validates string format, an
   ASCII pattern would forbid Unicode slugs, and the surveyed validators
   disagree on the allowed characters.
6. **Django's 50-character default**: rejected as too short; Wagtail and this
   library's other short strings use 255.

## Discussion Summary

Issue #115 lists `Slug` as an unimplemented proposal carried over from the
original `CHAT.md` design discussion (preserved in the README roadmap), with
`slug` and `title` as candidate fields. The issue asks for decisions on
generation/normalization, uniqueness, and indexing.

## Consequences

- Adds `Slug` to the SQLAlchemy, SQLModel (re-export), MongoEngine, and ODMantic
  adapters, each in its own `slug.py` and re-exported from the adapter's
  `__init__.py`, with tests under `tests/<framework>/` and an entry in
  `MIXIN_NAMES` in `tests/test_cross_framework_consistency.py`.
- Consumers must populate `slug` themselves and add the unique index that fits
  their scope. Without one, duplicate slugs are accepted.
- On SQL, an empty slug is accepted unless the consumer adds a check
  constraint; the document adapters reject it.
- SQLModel inherits the SQLAlchemy column as-is, with the same limitations
  as the other re-exported mixins.
- No changes to existing mixins and no migration for existing users.
- Slug history and redirects remain a possible future RFC.

## Implementation Notes

To be filled in after implementation merges.

## References

- https://github.com/hasansezertasan/opinionated-mixins/issues/115
- https://github.com/hasansezertasan/opinionated-mixins/pull/130
- https://docs.djangoproject.com/en/stable/ref/models/fields/#slugfield
- https://docs.djangoproject.com/en/stable/ref/validators/
- https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields
- https://docs.wagtail.org/en/stable/reference/pages/model_reference.html
- https://developer.wordpress.org/rest-api/reference/posts/
- https://developer.wordpress.org/reference/functions/wp_unique_post_slug/
- https://norman.github.io/friendly_id/file.Guide.html
- https://github.com/spatie/laravel-sluggable
- https://docs.strapi.io/cms/backend-customization/models
- https://shopify.dev/docs/api/admin-graphql/latest/objects/Product
- https://github.com/un33k/python-slugify
