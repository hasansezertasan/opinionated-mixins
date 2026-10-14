# Prior Art: Settled Names, Open Candidates, Lessons

## Settled field names (reuse under rule 2)

- Timestamps: `created_at` (RFC-0001), `updated_at` (RFC-0002). Activity/Notification reuse `created_at` over Django's `timestamp`.
- Flags: `is_active` (RFC-0003); prefer positive booleans.
- Identity: SQL-only `IntegerID` (RFC-0004); `UUIDID` for SQLAlchemy/SQLModel, native IDs on Mongo (RFC-0005).
- Messaging: `title` + `content` (Announcement RFC-0008; reused by Feedback RFC-0010, Template RFC-0011, Lead RFC-0012, Notification RFC-0006). Never re-add `title` to a mixin that composes with these (RFC-0014 alternative 2).
- Person core: `first_name`/`middle_name`/`last_name`, `phone_number`, `email` (254, RFC 5321), `street_address`, `postal_code`, `city`, `country` (ISO 3166-1 alpha-2), `date_of_birth`, `bio` (RFC-0009).
- Activity: `verb`, `description`, `data`, `actor_type`/`actor_id` (required), `target_type`/`target_id`, `action_object_type`/`action_object_id`, `public`, `created_at` (RFC-0007, from issue #42; W3C Activity Streams + django-notifications + django-activity-stream).
- Notification: `notification_type`, `level` (`info`/`success`/`warning`/`error`), `title`, `description`, `data`, `actor_type`/`actor_id`, `action_url`, `group_key`, `seen_at`/`read_at`, `created_at` (RFC-0006, from issue #41; django-notifications + Laravel + Rails Noticed + GitHub API). Recipient stays framework-idiomatic, not prescribed.
- Slug: `slug`, `String(255)`, required, not unique by default, no generation/normalization/validation (RFC-0014, from umbrella #115; Django + Wagtail + friendly_id + spatie + Strapi vs Shopify `handle` outlier).

## Open candidates (issue #115 umbrella)

Partial coverage (extend/reuse first): **SoftDelete** (`deleted_at`/`deleted_by` beyond `IsActive`), **Audit** (`created_by`/`updated_by` vs Activity log), **Address** (lines, state/province beyond Person), **Contact** (mobile/fax, extra URLs beyond Person/Lead), **Status** (general change reason/timestamp/actor vs Feedback/Lead enums), **Metadata** (portable tags/JSON naming; `metadata` is SQLAlchemy-reserved).
Unimplemented: **Version** (`version`, `is_latest`, `parent_id`), **Priority** (`priority`, `order`), **Expiration** (`expires_at`, `is_expired`).
Deferred frameworks (storage-only scope per #34, revisit in discussion #123): TortoiseORM, Beanie, Pydantic, dataclasses, WTForms.

## Lessons from resolved issues/PRs

- **Symmetry across related mixins** (issue #44): Activity made actor fields required, exposing Notification's nullable asymmetry (4/5 references required actor). Check sibling mixins for matching nullability/defaults.
- **Indexes are consumer concerns** (issue #121, PR #130, RFC-0014): no `index=True` in mixins; document per-field index recipes (`__table_args__`, MongoEngine `meta["indexes"]` with `"cls": False`, ODMantic `model_config["indexes"]`); note collation, NULL-scoping, and soft-delete caveats.
- **Behavior varies -> document, don't bake in** (RFC-0014): generation, uniqueness scope, history/redirects out of scope with recommendations; no string-format validation (rejects valid Unicode, references disagree); empty-string and length enforcement differ per backend, so state the asymmetry.
- **No DB-side defaults** (RFC-0001/0005): `now()`/`gen_random_uuid()` rejected for portability; use application-side defaults.
- **No framework-coupled mechanisms** (RFC-0007): `GenericForeignKey` rejected; use portable `*_type`/`*_id` pairs.
- **Mixin purity** (issues #30, #39): no `BaseModel` inheritance in mixins; ODMantic needs the metaclass idiom (`_base.py`); verify composition per framework, not field definitions alone.
- **Typing without runtime cost** (issue #165, PR #166/RFC-0015): `Mapped[...]` lives in `TYPE_CHECKING` only with a drift test; runtime annotations break SQLModel composition (`PydanticSchemaGenerationError`); README must note the schema-only caveat.
- **Consensus process itself** (issues #47, #122; PR #71): rationale must survive offline (Discussion Summary, Alternatives, Reference Implementation in-repo); 13 backfilled RFCs (0001-0013) reconstruct decisions; criteria live in `docs/rfcs/README.md`.
