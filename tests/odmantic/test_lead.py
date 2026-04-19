from opinionated_mixins.contrib.odmantic import Lead

LEAD_ANNOTATIONS = {
    "title",
    "salutation",
    "job_title",
    "company_name",
    "website",
    "linkedin_url",
    "status",
    "source",
    "industry",
    "rating",
    "opportunity_amount",
    "currency",
    "probability",
    "close_date",
    "last_contacted",
    "next_follow_up",
    "description",
    "is_active",
}


class TestODManticLead:
    def test_has_expected_annotations(self) -> None:
        for field_name in LEAD_ANNOTATIONS:
            assert field_name in Lead.__annotations__

    def test_optional_fields_default_none(self) -> None:
        for field_name in ("title", "status", "source", "rating", "close_date"):
            field_info = getattr(Lead, field_name).pydantic_field_info
            assert field_info.default is None, f"{field_name} should default to None"

    def test_probability_default(self) -> None:
        field_info = Lead.probability.pydantic_field_info
        assert field_info.default == 0

    def test_is_active_default(self) -> None:
        field_info = Lead.is_active.pydantic_field_info
        assert field_info.default is True
