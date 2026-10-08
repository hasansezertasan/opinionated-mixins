"""Tests for values passed through ODMantic BSON date conversion."""

import datetime

import pytest

from opinionated_mixins.contrib.odmantic._base import date_to_datetime_for_bson


@pytest.mark.parametrize(
    "value",
    [
        None,
        "2026-10-08",
        42,
        datetime.datetime(2026, 10, 8, tzinfo=datetime.timezone.utc),
    ],
)
def test_date_conversion_preserves_non_date_values(value: object) -> None:
    """Only date-only values should be replaced during BSON conversion."""
    assert date_to_datetime_for_bson(value) is value
