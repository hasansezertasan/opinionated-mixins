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

A `Slug` mixin providing a single required `slug` string (1–255 characters):
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
| Django `SlugField` | `slug` (convention) | 50 | No (opt-in) | `title` via admin `prepopulated_fields` | https://docs.djangoproject.com/en/stable/ref/models/fields/#slugfield |
| Wagtail `Page` | `slug` | 255 | Among siblings, enforced in code | `title` when blank | https://docs.wagtail.org/en/stable/reference/pages/model_reference.html |
| WordPress | `post_name` (REST: `slug`) | 200 | Per post type / per parent, enforced in code | `title` | https://developer.wordpress.org/rest-api/reference/posts/ |
| Rails `friendly_id` | `slug` | — | Unique index recommended | `title` / `name` | https://norman.github.io/friendly_id/file.Guide.html |
| Laravel `spatie/laravel-sluggable` | `slug` | configurable | Suffix-based, scope configurable | `title` | https://github.com/spatie/laravel-sluggable |
| Strapi `uid` | any (usually `slug`) | configurable | No (opt-in) | `targetField` | https://docs.strapi.io/cms/backend-customization/models |
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
  localized sites scope it per tenant or locale. Only friendly_id recommends a
  plain global unique index, and Django and Strapi leave uniqueness opt-in.
- **Generate once, do not regenerate.** Django's admin skips saved objects,
  friendly_id 5+ generates only when the slug is `nil`, and Shopify keeps the
  handle after a title change. spatie/laravel-sluggable regenerates by default
  but documents an opt-out. Changing slugs breaks URLs, so the libraries that do
  support it add a history or redirect layer (friendly_id `History`, Spatie
  self-healing URLs, Wagtail's `page_slug_changed` signal).
- **Format is lowercase ASCII with hyphens by default, with Unicode opt-in.**
  Django validates `[-a-zA-Z0-9_]` unless `allow_unicode=True`.
  `python-slugify` and Django's `slugify()` default to ASCII. Wagtail enables
  Unicode slugs. Strapi allows `[A-Za-z0-9-_.~]`.

## Design

### Fields

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
| `slug` | `str` | yes | — | 1–255 characters; not unique by default (see below) |

**Generation and normalization.** Out of scope. A plain mixin cannot portably
hook a source field across SQLAlchemy, MongoEngine, and ODMantic, and every
surveyed library treats generation as an application-level choice (which
source field, which slugify function, whether Unicode is allowed, collision
suffix strategy). Consumers set `slug` explicitly, typically with
`django.utils.text.slugify`, `python-slugify`, or an equivalent, once at
creation.

**Format validation.** None beyond length. SQLAlchemy cannot portably enforce
a regular expression across dialects, so a pattern would hold only in the
document adapters. Unicode slugs (Wagtail, localized sites) would also be
rejected by an ASCII pattern. The recommended format,
`^[a-z0-9]+(?:-[a-z0-9]+)*$`, is documented in docstrings.

**Uniqueness and indexing.** The column is not declared `unique`. Because the
correct scope varies (global, per parent, per type, per tenant, per locale), a
global unique constraint in the mixin would block valid scoped designs, and
dropping it would require overriding the column. Following the policy adopted
in #130, each adapter's docstring recommends the index to add:

- a unique index on `slug` when slugs are globally unique, or
- a composite unique constraint such as `(parent_id, slug)` or
  `(tenant_id, slug)` for scoped slugs.

Leaving uniqueness to the consumer also keeps the three adapters consistent:
ODMantic cannot declare uniqueness on a field (see RFC-0013's documented gap),
whereas a `unique=True` default would apply only to SQLAlchemy and
MongoEngine.

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
    for example with ``slugify(title)`` at creation. Recommended format:
    ``^[a-z0-9]+(?:-[a-z0-9]+)*$``.

    Indexing recommendations:
    - ``slug``: unique index recommended when slugs are globally unique, or a
      composite unique constraint for scoped slugs (for example per parent or
      per tenant).

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

    Indexing recommendations:
    - ``slug``: add ``{"fields": ["slug"], "unique": True}`` to ``meta["indexes"]``
      for globally unique slugs, or a compound unique index for scoped slugs.
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

    ODMantic does not declare uniqueness on fields; create a unique index on
    ``slug`` (or a compound one for scoped slugs) through the Motor collection.
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
3. **Global `unique=True` on the column (like `User.username`)**: rejected
   because uniqueness scope varies (WordPress, Wagtail, multi-tenant, i18n), and
   a column-level constraint cannot be narrowed without overriding the column.
   It is the main open question for review. If accepted instead, ODMantic would
   carry the same documented gap as RFC-0013.
4. **Auto-generate from a source field on insert**: rejected. It needs
   framework-specific event hooks (SQLAlchemy `before_insert`, MongoEngine
   `clean`, a Pydantic validator), a slugify dependency, and a collision
   strategy, none of which a dependency-free plain mixin can provide
   consistently.
5. **Regex validation in the document adapters**: rejected. SQLAlchemy cannot
   enforce it portably, which would make behavior diverge across adapters, and
   it would forbid Unicode slugs.
6. **Django's 50-character default**: rejected as too short; Wagtail and this
   library's other short strings use 255.

## Discussion Summary

Issue #115 lists `Slug` as an unimplemented proposal from the original design
discussion, with `slug` and `title` as candidate fields, and asks for decisions
on generation/normalization, uniqueness, and indexing. This RFC answers each
one: no generation, a documented format, uniqueness and indexing documented
rather than enforced, and no `title` field.

## Consequences

- Adds `Slug` to the SQLAlchemy, SQLModel (re-export), MongoEngine, and ODMantic
  adapters, each in its own `slug.py` and re-exported from the adapter's
  `__init__.py`, with tests under `tests/<framework>/`.
- Consumers must populate `slug` themselves and add the unique index that fits
  their scope. Without one, duplicate slugs are accepted.
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
