# RFC Process

This directory holds the **Request for Comments (RFC)** records for
`opinionated-mixins`. Every new mixin, new field on an existing mixin, new
framework adoption, and breaking change is documented here as a markdown file.

The merged RFC is the canonical, **offline-readable** spec. It should be
readable on a subway, by an AI agent without GitHub access, or by a
contributor years from now — without needing to open a single GitHub issue.

## What is an RFC?

An RFC is a proposal document that captures **what** is being built, **why**,
and **what alternatives were rejected**. It differs from the other artifacts
in this repo:

| Artifact | Answers | Lives |
| -------- | ------- | ----- |
| **Issue** | "Someone wants X" (intake, optional) | GitHub |
| **RFC** | "Should we build X, and why this way?" | this directory (in-repo) |
| **PR** | "Here is the code for X" | git history |

Because the RFC lives in the repo, its rationale survives comment deletion,
GitHub outages, and offline work — the original problems this process solves.

## When is an RFC required?

**Required** for:

- New mixin classes
- New fields on existing mixins
- New framework support
- Breaking changes to existing mixins

**Not required** for:

- Bug fixes
- Test improvements
- Documentation updates
- Tooling / CI changes

Non-mixin decisions (tooling, build backend, repo layout) do not need an RFC.
If enough orphan decisions accumulate, a separate `docs/decisions/` (ADR)
directory may be added later.

## Consensus criteria

Every naming, enum-value, default, and behavior decision in an RFC is made
against these criteria. They formalize the consensus principles informed by
RFC-0001 through RFC-0014. (RFCs accepted before these criteria were codified
are grandfathered; see [When a convention is settled](#when-a-convention-is-settled).)

### References

- **At least three independent references** per field-naming or enum-value
  decision. Independent means a different project, vendor, or standards body.
  These count once:
  - versions of the same standard, such as Activity Streams 1.0 and 2.0;
  - several objects or pages from one vendor, such as Salesforce Lead and
    Opportunity;
  - several classes from one framework, such as two Django models.
- A reference is a **named, linkable source**. Rows such as "General" or
  "common practice" do not count.
- Mix kinds where the domain allows. Useful kinds are frameworks and ORMs
  (Django, Rails, Laravel), widely used packages, public APIs (GitHub,
  Zendesk), and standards (IETF RFCs, ISO, W3C, schema.org).
- If a domain genuinely has fewer than three independent sources, state and
  justify this in the Research section instead of padding the table.

### Resolving conflicts

When references disagree, apply these rules in order. The first rule that
decides wins.

1. **Hard constraints.**
   - Maintain consistent public behavior across adapters, adapted to each
     framework's idioms. Where framework limitations prevent identical
     behavior, document the asymmetry under Consequences (as RFC-0002 did for
     SQLAlchemy-only `onupdate`). Storage-specific mixins (such as SQL-only
     `IntegerID` in RFC-0004) are restricted to their applicable adapters.
   - Database-side defaults (such as server-side `func.now()` or
     `gen_random_uuid()`) are rejected for backend portability (RFC-0001,
     RFC-0005).
   - Reject framework-coupled mechanisms that cannot compose cleanly across
     adapters, such as `GenericForeignKey` (RFC-0007).
   - Where a published standard fixes a limit or format, follow it. Examples
     are the RFC 5321 email length and ISO 3166-1 country codes (RFC-0009).
     (Note that published standards dictate formats and limits; when naming
     conflicts arise between a standard and prevailing application code,
     application conventions can prevail under consensus, as `first_name` won
     over schema.org's `givenName` in RFC-0009.)
2. **Consistency with accepted RFCs.** If an accepted mixin already names the
   concept, reuse that name, even when external references prefer another. For
   example, `content` was established in RFC-0008 and reused in RFC-0010 and
   RFC-0011 over `body`; `created_at` was established in RFC-0001 and reused in
   RFC-0007 over Django's `timestamp`.
3. **Majority of independent references.** Count the Research table. A strict
   majority (>50% of independent references) decides. Name the outliers. For
   example, five of seven sources use `slug`, while Shopify's `handle` and
   WordPress's internal `post_name` are outliers (RFC-0014).
4. **Clarity.** Apply this when references are tied, when no majority emerges,
   or when the majority name is ambiguous:
   - positive booleans (`is_active`, not `is_disabled`);
   - names that state their contract (`hashed_password`);
   - nullable timestamps over booleans when *when* matters;
   - enums over free-form strings;
   - `Decimal` for money.

For each contested choice, state in the RFC which rule decided it.

### Enum values

An enum is surveyed across at least three independent references. The enum
contains the union of values that appear in at least two independent
references, with one member per meaning. Map synonyms to that member and say
so, as Bootstrap's `danger` maps to `error` (RFC-0008). A value found in only
one source needs an explicit justification, as `CRITICAL` from syslog has in
RFC-0006.

### No consensus

Sometimes references disagree on a behavior or convention and none of the rules
above decides it. Do not pick a side arbitrarily. Either leave the behavior to
the consumer or defer it, and record the outcome under Alternatives Considered.
RFC-0014, for example, leaves both slug generation and uniqueness scope to
the consumer.

### When a convention is settled

An accepted RFC settles its decisions, and later RFCs follow them under
rule 2. New references alone do not reopen a settled name or value.
Backwards-compatible additions (such as adding an optional field or new enum
member) follow standard feature RFCs. Modifying or renaming an accepted field or
enum member requires a `breaking-change` RFC that supersedes the original.

RFCs accepted before these criteria were written are not rewritten retroactively.
They are revisited only through a superseding RFC.

## How to propose

### Path A — Direct RFC PR

For authors who have already done the research.

1. Pick the next number from [`INDEX.md`](INDEX.md).
2. Create a branch: `rfc/<slug>`.
3. Copy [`TEMPLATE.md`](TEMPLATE.md) to `XXXX-<slug>.md`.
4. Set `type:` in the frontmatter and fill the sections required for that type
   (see the table below).
5. Open a PR with the `rfc` label and one `status:*` label.

### Path B — Issue first

A lower-friction on-ramp for ideas that are not yet fully researched.

1. Open an issue using a proposal template (model / field / framework).
2. Discuss.
3. When the idea has traction, write the RFC PR (as in Path A) referencing the
   issue. Distill the discussion into the RFC's **Discussion Summary** section.

The issue step is **optional**. The RFC PR is the artifact that gets preserved.

## Status lifecycle

```
draft ──▶ proposed ──▶ accepted    (PR merged with status:accepted)
                   ├─▶ rejected    (PR merged with status:rejected, or closed)
                   ├─▶ deferred    (PR merged with status:deferred)
                   └─▶ withdrawn   (PR merged with status:withdrawn)

accepted ──▶ superseded            (when a newer RFC's `supersedes:` points here)
```

Merging `rejected` / `deferred` / `withdrawn` RFCs is at the maintainer's
discretion. Merging preserves the rationale offline; closing keeps the
directory tidy. Neither is mandatory.

## Labels

Every RFC PR carries:

- `rfc` — marks the PR as an RFC.
- Exactly one of `status:accepted`, `status:rejected`, `status:deferred`,
  `status:withdrawn`.

On merge, [`rfc.yml`](../../.github/workflows/rfc.yml) reads the `status:*`
label, writes it into the RFC frontmatter, stamps `github_pr` and `updated`,
and regenerates [`INDEX.md`](INDEX.md). Do not hand-edit `INDEX.md` — it is
derived data.

`status:superseded` is **not** a PR label. It is derived automatically: when a
new RFC declares `supersedes: "NNNN"`, the workflow flips RFC-NNNN to
`superseded` and links the two.

To create these labels in the repository (idempotent):

```bash
scripts/create-rfc-labels.sh
```

## Section requirements by type

| Section | mixin | field | framework | breaking-change |
| ------- | ----- | ----- | --------- | --------------- |
| Summary | required | required | required | required |
| Motivation | required | required | required | required |
| Research → Field Naming | required | required | — | conditional |
| Research → Enum Values | conditional | conditional | — | conditional |
| Research → Framework Adoption | — | — | required | — |
| Design → Fields | required | required | — | required |
| Design → Reference Implementation | required | required | required | required |
| Design → Framework Mixin Idioms | — | — | required | — |
| Alternatives Considered | required | required | required | required |
| Discussion Summary | conditional | conditional | conditional | conditional |
| Consequences | required | required | required | required |
| Implementation Notes | post-merge | post-merge | post-merge | post-merge |

"conditional" = required when the RFC touches that area (e.g. Enum Values is
required only when the RFC adds an enum).

## After acceptance

Implementation happens in **separate** PR(s) that reference the RFC number.
Once implementation merges, update the RFC's **Implementation Notes** section
with any decisions that deviated from the original design.

## Backfilling

Mixins that predate this process have retroactive RFCs documenting the
decisions already made. Their `status` is `accepted` and `github_pr` points at
the original implementation PR. One mixin gets one RFC, even when several
mixins shipped in a single batch PR — each has independent rationale and may
evolve separately.

## Regenerating the index locally

```bash
python scripts/rfc.py index
```

This is what the workflow runs; you can run it locally to preview the index
after adding an RFC.
