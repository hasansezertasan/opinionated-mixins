# RFC Workflow (from `docs/rfcs/README.md`)

## Artifact split

| Artifact | Answers | Lives |
| -------- | ------- | ----- |
| Issue | "Someone wants X" (optional intake) | GitHub |
| RFC | "Should we build X, and why this way?" | `docs/rfcs/` (offline-readable) |
| PR | "Here is the code for X" | git history |

## Paths

- **Path A (direct RFC PR):** pick next number from `INDEX.md`; copy `TEMPLATE.md` to `XXXX-<slug>.md`; set `type:`; fill required sections; open PR with `rfc` + one `status:*` label. Use a branch name that passes CI's branch-name check (conventional prefixes only, e.g. `feature/rfc-<slug>`): the RFC README's `rfc/<slug>` suggestion is rejected by `check-branch-name.yml`.
- **Path B (issue first):** open issue with a proposal template (`model_proposal.md` / `field_proposal.md` / `framework_proposal.md`); discuss; write RFC PR referencing the issue; distill discussion into **Discussion Summary**.

## RFC required for

New mixin classes, new fields on existing mixins, new framework support, breaking changes. Not required for bug fixes, tests, docs, tooling/CI.

## Labels and lifecycle

- Every RFC PR carries `rfc` plus exactly one of `status:accepted`, `status:rejected`, `status:deferred`, `status:withdrawn`. `status:superseded` is derived when a new RFC declares `supersedes:`.
- Lifecycle: `draft -> proposed -> accepted | rejected | deferred | withdrawn`; `accepted -> superseded` via a newer RFC. Merging rejected/deferred/withdrawn RFCs is the maintainer's call.
- On merge, `rfc.yml` stamps `status`, `github_pr`, `updated` and regenerates `INDEX.md`. Never hand-edit `INDEX.md`; preview with `python scripts/rfc.py index`. Create labels with `scripts/create-rfc-labels.sh`. Caveat: the workflow cannot push to protected `main` without a bypass token, so run the sync by hand inside the RFC PR before merging (`set-status`, then `sync-supersedes`, then `index`), as documented in the `rfc.yml` header — otherwise the merged RFC keeps its draft status and `INDEX.md` goes stale.

## Section requirements by type

| Section | mixin | field | framework | breaking-change |
| ------- | ----- | ----- | --------- | --------------- |
| Summary | required | required | required | required |
| Motivation | required | required | required | required |
| Research: Field Naming | required | required | — | conditional |
| Research: Enum Values | conditional | conditional | — | conditional |
| Research: Framework Adoption | — | — | required | — |
| Design: Fields | required | required | — | required |
| Design: Reference Implementation | required | required | required | required |
| Design: Framework Mixin Idioms | — | — | required | — |
| Alternatives Considered | required | required | required | required |
| Discussion Summary | conditional | conditional | conditional | conditional |
| Consequences | required | required | required | required |
| Implementation Notes | post-merge | post-merge | post-merge | post-merge |

## Implementation layering

- Mixins are plain classes composed with a framework base; never inherit a framework base in the mixin.
- One file per mixin per adapter, re-exported from that adapter's `__init__.py`. Shared enums live in `src/opinionated_mixins/enums.py`.
- SQLModel re-exports SQLAlchemy implementations (import-linter enforces: `sqlmodel` may only re-export `sqlalchemy`; MongoEngine and ODMantic stay independent). A native SQLModel adapter needs an architecture update.
- SQLAlchemy columns use `Column(...)`. A `Mapped[...]`-in-`TYPE_CHECKING` typing pattern was proposed (issue #165, PR #166) but that PR closed unmerged and no RFC-0015 exists in the repo — treat it as pending work, not settled guidance, and never cite RFC-0015 as an accepted spec. SQLModel composition treats re-exported mixins as schema-only (issue #167 tracks the native-adapter follow-up).
- Tests mirror `src` under `tests/<framework>/`; cross-framework consistency lives in `tests/test_cross_framework_consistency.py` (`MIXIN_NAMES`).
- After implementation merges, fill the RFC's **Implementation Notes** with deviations.
