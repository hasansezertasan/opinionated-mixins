from opinionated_mixins.contrib.mongoengine import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus


class TestMongoEngineLead:
    def test_has_title_field(self) -> None:
        assert Lead.title.required is False
        assert Lead.title.max_length == 255

    def test_has_status_field(self) -> None:
        assert Lead.status.required is False
        assert Lead.status.choices == [s.value for s in LeadStatus]

    def test_has_source_field(self) -> None:
        assert Lead.source.required is False
        assert Lead.source.choices == [s.value for s in LeadSource]

    def test_has_rating_field(self) -> None:
        assert Lead.rating.required is False
        assert Lead.rating.choices == [r.value for r in LeadRating]

    def test_has_scalar_fields(self) -> None:
        for field_name in (
            "title",
            "salutation",
            "job_title",
            "company_name",
            "website",
            "linkedin_url",
            "industry",
            "opportunity_amount",
            "currency",
            "probability",
            "close_date",
            "last_contacted",
            "next_follow_up",
            "description",
            "is_active",
        ):
            assert hasattr(Lead, field_name), f"Missing field: {field_name}"
