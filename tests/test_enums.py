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
            "GENERAL",
            "INFO",
            "WARNING",
            "SUCCESS",
            "ERROR",
            "MAINTENANCE",
            "UPDATE",
            "EVENT",
        ]
        assert [c.value for c in AnnouncementCategory] == expected

    def test_str_mixin(self) -> None:
        assert AnnouncementCategory.GENERAL == "GENERAL"
        assert isinstance(AnnouncementCategory.INFO, str)

    def test_lookup_by_value(self) -> None:
        assert AnnouncementCategory("WARNING") is AnnouncementCategory.WARNING


class TestTemplateFormat:
    def test_values(self) -> None:
        expected = ["PLAIN", "HTML", "MARKDOWN"]
        assert [c.value for c in TemplateFormat] == expected

    def test_str_mixin(self) -> None:
        assert TemplateFormat.PLAIN == "PLAIN"
        assert isinstance(TemplateFormat.HTML, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateFormat("HTML") is TemplateFormat.HTML


class TestLeadStatus:
    def test_values(self) -> None:
        expected = ["ASSIGNED", "IN_PROCESS", "CONVERTED", "RECYCLED", "CLOSED"]
        assert [s.value for s in LeadStatus] == expected

    def test_str_mixin(self) -> None:
        assert LeadStatus.ASSIGNED == "ASSIGNED"
        assert isinstance(LeadStatus.CONVERTED, str)

    def test_lookup_by_value(self) -> None:
        assert LeadStatus("CONVERTED") is LeadStatus.CONVERTED


class TestLeadSource:
    def test_values(self) -> None:
        expected = [
            "CALL",
            "EMAIL",
            "EXISTING_CUSTOMER",
            "PARTNER",
            "PUBLIC_RELATIONS",
            "CAMPAIGN",
            "OTHER",
        ]
        assert [s.value for s in LeadSource] == expected

    def test_str_mixin(self) -> None:
        assert LeadSource.CALL == "CALL"
        assert isinstance(LeadSource.EMAIL, str)

    def test_lookup_by_value(self) -> None:
        assert LeadSource("PARTNER") is LeadSource.PARTNER


class TestLeadRating:
    def test_values(self) -> None:
        expected = ["HOT", "WARM", "COLD"]
        assert [r.value for r in LeadRating] == expected

    def test_str_mixin(self) -> None:
        assert LeadRating.HOT == "HOT"
        assert isinstance(LeadRating.WARM, str)

    def test_lookup_by_value(self) -> None:
        assert LeadRating("COLD") is LeadRating.COLD


class TestTemplateType:
    def test_values(self) -> None:
        expected = ["EMAIL", "SMS", "PUSH", "OTHER"]
        assert [c.value for c in TemplateType] == expected

    def test_str_mixin(self) -> None:
        assert TemplateType.EMAIL == "EMAIL"
        assert isinstance(TemplateType.SMS, str)

    def test_lookup_by_value(self) -> None:
        assert TemplateType("PUSH") is TemplateType.PUSH
