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
