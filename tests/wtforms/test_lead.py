from opinionated_mixins.contrib.wtforms import Lead
from wtforms import Form


class LeadForm(Lead, Form):  # type: ignore[misc]
    pass


LEAD_FIELDS = {
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


class TestWTFormsLead:
    def test_has_fields(self) -> None:
        form = LeadForm()
        for field_name in LEAD_FIELDS:
            assert field_name in form._fields, f"Missing field: {field_name}"

    def test_valid_submission_minimal(self) -> None:
        form = LeadForm(data={})
        assert form.validate()

    def test_valid_submission_with_data(self) -> None:
        form = LeadForm(
            data={
                "title": "Dr.",
                "job_title": "CTO",
                "status": "ASSIGNED",
                "source": "EMAIL",
                "rating": "HOT",
            },
        )
        assert form.validate()
