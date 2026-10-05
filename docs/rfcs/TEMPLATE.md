---
rfc: "XXXX"
title: <Title>
type: mixin # mixin | field | framework | breaking-change
status: draft # draft | proposed | accepted | rejected | deferred | withdrawn | superseded
created: YYYY-MM-DD # ISO date when the RFC PR is opened
updated: YYYY-MM-DD # ISO date of the last status change
author: <github-username>
github_issue: null # originating issue number, or null for the direct path
github_pr: null # auto-filled by the workflow on merge
supersedes: null # RFC number this replaces (e.g. "0003"), or null
superseded_by: null # RFC number that replaces this one, or null
---

# RFC-XXXX: <Title>

> Delete section-guidance blockquotes (like this one) before opening the PR.
> See [`README.md`](README.md) for which sections are required for your `type`.

## Summary

> One paragraph. What is being proposed?

## Motivation

> Why does this matter? What problem does it solve? Reference real use cases.
> Cite the originating issue if applicable.

## Research

> Industry-consensus check. Minimum **3** real-world references for any field
> naming or enum-value decision. This is the project's "research first,
> implement second" rule made durable.

### Field Naming

> Required for `mixin` and `field` RFCs.

| Source | Field Names Used | Link |
| ------ | ---------------- | ---- |
|        |                  |      |

### Enum Values

> Required only if this RFC introduces or changes an enum.

| Source | Field | Values |
| ------ | ----- | ------ |
|        |       |        |

### Framework Adoption

> Required only for `framework` RFCs.

| Metric                 | Value | Link |
| ---------------------- | ----- | ---- |
| GitHub stars           |       |      |
| PyPI monthly downloads |       |      |
| Last release           |       |      |

## Design

### Fields

> Required for `mixin`, `field`, and `breaking-change` RFCs.

| Field | Python Type | Required | Default | Constraints |
| ----- | ----------- | -------- | ------- | ----------- |
|       |             |          |         |             |

### Enum Additions

> Include only if this RFC adds or changes an enum. Show the proposed
> `enums.py` addition as a code block.

```python
# src/opinionated_mixins/enums.py
```

### Reference Implementation

> Required. Per-framework code blocks. SQLModel re-exports SQLAlchemy, so it
> does not need its own block unless it deliberately diverges.

```python
# SQLAlchemy
```

```python
# MongoEngine
```

```python
# ODMantic
```

### Framework Mixin Idioms

> Required only for `framework` RFCs. How does the new framework express
> mixins — plain class, abstract base, decorator? Show an example.

## Alternatives Considered

> Each alternative with a one-line rejection reason.

1. **<Alternative>** — rejected because ...

## Discussion Summary

> Distill the key points from the originating issue/PR discussion so the RFC
> is self-contained offline. Skip if there was no prior discussion.

## Consequences

> - What becomes possible after this RFC?
> - What new constraints does it impose?
> - What migration is required for existing users?
> - Which contrib modules need updates?

## Implementation Notes

> Filled in **after** implementation merges. Records decisions made during the
> build that deviated from this RFC, or details discovered while implementing.

## References

- <links to issue, PR, external docs cited in Research>
