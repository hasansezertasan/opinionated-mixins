import dataclasses

from opinionated_mixins.contrib.dataclasses import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus


class TestDataclassesFeedback:
    def test_is_dataclass(self) -> None:
        assert dataclasses.is_dataclass(Feedback)

    def test_create_with_defaults(self) -> None:
        obj = Feedback(subject="Bug report", content="Something broke")
        assert obj.subject == "Bug report"
        assert obj.content == "Something broke"
        assert obj.category == FeedbackCategory.OTHER
        assert obj.status == FeedbackStatus.PENDING

    def test_create_with_explicit_values(self) -> None:
        obj = Feedback(
            subject="Feature idea",
            content="Add dark mode",
            category=FeedbackCategory.FEATURE,
            status=FeedbackStatus.RESOLVED,
        )
        assert obj.category == FeedbackCategory.FEATURE
        assert obj.status == FeedbackStatus.RESOLVED

    def test_fields(self) -> None:
        fields = {f.name for f in dataclasses.fields(Feedback)}
        assert fields == {"subject", "content", "category", "status"}
