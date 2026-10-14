---
name: propose-rfc
description: Recommend a new mixin, field, framework adapter, or breaking change in the opinionated-mixins repo via its RFC process. Use when asked to propose, suggest, recommend, draft an RFC for, or design a mixin (e.g. SoftDelete, Address, Audit), add a field, support a framework (e.g. TortoiseORM, Beanie), or change an accepted field. Guides research with 3+ independent references, consensus-rule resolution, and RFC drafting.
---

# Propose RFC

Recommend storage-layer model contracts (ORM/ODM mixins) the way this repo accepts them: research first, RFC second, code last.

## Workflow

Follow these steps in order. Stop early only when the question is answered without a new proposal.

### 1. Check settled ground before proposing

- Read `docs/rfcs/INDEX.md` and any accepted RFC touching the concept. Under consensus rule 2, an accepted name wins even when external sources prefer another (`content` over `body`, `created_at` over `timestamp`, `first_name` over `givenName`).
- Check issue #115 (umbrella): it lists open candidates (SoftDelete, Audit, Address, Contact, Status, Metadata, Version, Priority, Expiration) with existing-coverage notes, plus deferred frameworks. Reuse or extend an existing mixin where it fits.
- New references alone never reopen a settled name. Renames need a `breaking-change` RFC that supersedes the original.
- See [prior-art.md](references/prior-art.md) for the settled-name index and reusable lessons from past issues/PRs.

### 2. Pick Path A or Path B

- **Path A (direct RFC PR):** author already did the research. Pick next number from `INDEX.md`, copy `docs/rfcs/TEMPLATE.md` to `XXXX-<slug>.md`, set `type:`, open PR with `rfc` + one `status:*` label. Branch naming caveat: the RFC README suggests `rfc/<slug>`, but CI's branch-name check only accepts conventional prefixes — use a conforming branch such as `feature/rfc-<slug>` until the two conventions are reconciled.
- **Path B (issue first):** idea without research. Open an issue with a proposal template (`model` / `field` / `framework` under `.github/ISSUE_TEMPLATE/`), discuss, then write the RFC PR distilling discussion into **Discussion Summary** so the RFC reads offline.
- Never implement before the RFC is accepted. Implementation lands in separate PRs referencing the RFC number.
- See [rfc-workflow.md](references/rfc-workflow.md) for labels, lifecycle, section table, and layering rules.

### 3. Research to the consensus bar

- Gather **at least 3 independent, named, linkable references** per field-naming or enum-value decision. Different project, vendor, or standards body; versions of one standard or pages of one vendor count once. Mix kinds (frameworks/ORMs, packages, public APIs, standards) where the domain allows. Genuinely fewer than 3: state and justify instead of padding.
- For enums, survey values across the same references; include the union of values appearing in at least two sources, one member per meaning, synonyms mapped. Single-source values need explicit justification.
- Resolve disagreements with the rules in order; state which rule decided each contested choice. No rule decides: leave to consumer or defer, recorded under Alternatives Considered.
- See [consensus.md](references/consensus.md) for the full rule order and enum policy.

### 4. Draft the RFC

- Copy `docs/rfcs/TEMPLATE.md`; delete guidance blockquotes; fill sections required for the `type` (see [rfc-workflow.md](references/rfc-workflow.md)).
- Design fields with the hard-constraints checklist: cross-adapter behavior parity, no DB-side defaults, no framework-coupled mechanisms, follow published limits/formats, positive booleans, nullable timestamps when *when* matters, enums over free strings, `Decimal` for money. Indexing is per adapter: SQLAlchemy sets no `index=True` (document per-field index recipes in docstrings instead), while document adapters follow their accepted RFCs' precedent (MongoEngine Activity/Notification declare `index=True` on query fields) — let the RFC decide indexing per field and adapter.
- Give rejected options a one-line reason under Alternatives Considered. Record generation/normalization, uniqueness scope, and history as out-of-scope with recommendations where past RFCs did (e.g. RFC-0014).
- Keep mixins plain classes (never inherit a framework base); one file per mixin per adapter, re-exported from the adapter `__init__`; SQLModel re-exports SQLAlchemy unless a native adapter is RFC-accepted; shared enums go in `src/opinionated_mixins/enums.py`; tests mirror under `tests/<framework>/`.

### 5. Validate before opening the PR

- Run `python scripts/rfc.py index` to preview the generated index; never hand-edit `INDEX.md`.
- Confirm frontmatter (`rfc`, `title`, `type`, `status: draft|proposed`, `created`, `author`, `github_issue` or null) and required sections for the type.
- Confirm every contested choice names its deciding rule, every alternative has a rejection reason, and out-of-scope behavior is explicit rather than silently unspecified.

## Anti-patterns

- Proposing Pydantic/dataclass/WTForms contracts without addressing the storage-only scope (#34, discussion #123): flag the scope question first.
- Baking in generation hooks, global uniqueness, format regexes, or `index=True` to settle what references leave varied: document and defer instead.
- Reopening settled names with fresh references instead of a superseding breaking-change RFC.
