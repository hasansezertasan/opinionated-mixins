"""Cross-module mixins using postponed annotations and module-local types."""

from __future__ import annotations

from odmantic import EmbeddedModel

from opinionated_mixins.contrib.odmantic import Person


class Address(EmbeddedModel):
    """Embedded type available only in the mixin's defining module."""

    street: str


class RelatedPerson(Person):
    """Mixin whose postponed annotation refers to a module-local type."""

    address: Address
