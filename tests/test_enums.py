from opinionated_mixins.enums import (
    AnnouncementCategory,
    LeadRating,
    LeadSource,
    LeadStatus,
    TemplateFormat,
    TemplateType,
)


class TestAnnouncementCategory:
    def test_values(self) -> None:
        expected = [
            "general",
            "info",
            "warning",
            "success",
            "error",
            "maintenance",
            "update",
            "event",
        ]
        assert [c.value for c in AnnouncementCategory] == expected

    def test_str_mixin(self) -> None:
        assert AnnouncementCategory.GENERAL == "general"
        assert isinstance(AnnouncementCategory.INFO, str)

    def test_lookup_by_value(self) -> None:
        assert AnnouncementCategory("warning") is AnnouncementCategory.WARNING


class TestTemplateFormat:
    def test_values(self) -> None:
        expected = ["plain", "html", "markdown"]
        assert [c.value for c in TemplateFormat] == expected

    def test_str_mixin(self) -> None:
        assert TemplateFormat.PLAIN == "plain"
        assert isinstance(TemplateFormat.HTML, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateFormat("html") is TemplateFormat.HTML


class TestLeadStatus:
    def test_values(self) -> None:
        expected = ["assigned", "in_process", "converted", "recycled", "closed"]
        assert [s.value for s in LeadStatus] == expected

    def test_str_mixin(self) -> None:
        assert LeadStatus.ASSIGNED == "assigned"
        assert isinstance(LeadStatus.CONVERTED, str)

    def test_lookup_by_value(self) -> None:
        assert LeadStatus("converted") is LeadStatus.CONVERTED


class TestLeadSource:
    def test_values(self) -> None:
        expected = [
            "call",
            "email",
            "existing_customer",
            "partner",
            "public_relations",
            "campaign",
            "other",
        ]
        assert [s.value for s in LeadSource] == expected

    def test_str_mixin(self) -> None:
        assert LeadSource.CALL == "call"
        assert isinstance(LeadSource.EMAIL, str)

    def test_lookup_by_value(self) -> None:
        assert LeadSource("partner") is LeadSource.PARTNER


class TestLeadRating:
    def test_values(self) -> None:
        expected = ["hot", "warm", "cold"]
        assert [r.value for r in LeadRating] == expected

    def test_str_mixin(self) -> None:
        assert LeadRating.HOT == "hot"
        assert isinstance(LeadRating.WARM, str)

    def test_lookup_by_value(self) -> None:
        assert LeadRating("cold") is LeadRating.COLD


class TestTemplateType:
    def test_values(self) -> None:
        expected = ["email", "sms", "push", "other"]
        assert [c.value for c in TemplateType] == expected

    def test_str_mixin(self) -> None:
        assert TemplateType.EMAIL == "email"
        assert isinstance(TemplateType.SMS, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateType("push") is TemplateType.PUSH
