# Consensus Criteria (from `docs/rfcs/README.md`)

Apply to every naming, enum-value, default, and behavior decision. State which rule decided each contested choice in the RFC.

## References

- Minimum **3 independent references** per field-naming or enum-value decision. Independent = different project, vendor, or standards body.
- Count once: versions of one standard (Activity Streams 1.0/2.0); several objects/pages of one vendor (Salesforce Lead + Opportunity); several classes of one framework (two Django models).
- A reference is a **named, linkable source**. "General" / "common practice" rows do not count.
- Mix kinds where the domain allows: frameworks/ORMs (Django, Rails, Laravel), widely used packages, public APIs (GitHub, Zendesk), standards (IETF, ISO, W3C, schema.org).
- Domain genuinely has fewer than 3 sources: state and justify in Research instead of padding.

## Resolving conflicts (first deciding rule wins)

1. **Hard constraints.**
   - Consistent public behavior across adapters, adapted to each framework's idioms; document asymmetries under Consequences (RFC-0002 did for SQLAlchemy-only `onupdate`). Storage-specific mixins (SQL-only `IntegerID`, RFC-0004) stay in applicable adapters.
   - Reject database-side defaults (`func.now()`, `gen_random_uuid()`) for backend portability (RFC-0001, RFC-0005).
   - Reject framework-coupled mechanisms that cannot compose across adapters (`GenericForeignKey`, RFC-0007).
   - Follow published standards for limits/formats: RFC 5321 email length, ISO 3166-1 country codes (RFC-0009). Note: standards fix formats/limits, but application conventions can win naming under rule 3 (`first_name` over schema.org `givenName`, RFC-0009).
2. **Consistency with accepted RFCs.** Reuse the accepted name even when external references prefer another: `content` (RFC-0008, reused in RFC-0010/0011) over `body`; `created_at` (RFC-0001, reused in RFC-0007) over Django's `timestamp`.
3. **Majority of independent references.** Strict majority (>50%) of the Research table decides; name the outliers (RFC-0014: five of seven use `slug`; Shopify `handle` and WordPress internal `post_name` are outliers).
4. **Clarity.** Ties, no majority, or ambiguous majority name: positive booleans (`is_active`, not `is_disabled`); names stating their contract (`hashed_password`); nullable timestamps over booleans when *when* matters; enums over free-form strings; `Decimal` for money.

## Enum values

- Survey values across at least 3 independent references.
- Include the union of values appearing in **at least two** sources, one member per meaning; map synonyms (`danger` -> `error`, RFC-0008).
- Single-source values need explicit justification (`CRITICAL` from syslog, RFC-0006).

## No consensus

- No rule decides: do not pick arbitrarily. Leave behavior to the consumer or defer it; record under Alternatives Considered. RFC-0014 leaves slug generation and uniqueness scope to the consumer.

## Settled conventions

- Accepted RFCs settle their decisions; later RFCs follow them under rule 2.
- Backwards-compatible additions (optional field, new enum member) use a standard feature RFC.
- Modifying/renaming an accepted field or enum member needs a `breaking-change` RFC superseding the original. Pre-criteria RFCs are revisited only via supersession, never rewritten.
