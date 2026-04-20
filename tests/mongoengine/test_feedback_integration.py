"""Integration tests for MongoEngine Feedback mixin."""

from mongoengine import Document

from opinionated_mixins.contrib.mongoengine import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus


class MyFeedback(Feedback, Document):
    """Test model composing Feedback with Document."""

    meta = {"collection": "test_feedbacks"}


class TestFeedbackIntegration:
    """Test Feedback mixin composition, instantiation, and roundtrip."""

    def test_create_with_defaults(self) -> None:
        obj = MyFeedback(subject="Bug report", content="Something broke")
        obj.save()
        loaded = MyFeedback.objects.first()
        assert loaded is not None
        assert loaded.subject == "Bug report"
        assert loaded.content == "Something broke"
        assert loaded.category == FeedbackCategory.OTHER.value
        assert loaded.status == FeedbackStatus.PENDING.value

    def test_create_with_explicit_values(self) -> None:
        obj = MyFeedback(
            subject="Feature request",
            content="Add dark mode",
            category=FeedbackCategory.FEATURE.value,
            status=FeedbackStatus.REVIEWED.value,
        )
        obj.save()
        loaded = MyFeedback.objects.first()
        assert loaded.category == FeedbackCategory.FEATURE.value
        assert loaded.status == FeedbackStatus.REVIEWED.value

    def test_roundtrip_preserves_all_fields(self) -> None:
        obj = MyFeedback(
            subject="Improvement",
            content="Faster loading",
            category=FeedbackCategory.IMPROVEMENT.value,
            status=FeedbackStatus.RESOLVED.value,
        )
        obj.save()
        loaded = MyFeedback.objects.first()
        assert loaded.subject == "Improvement"
        assert loaded.content == "Faster loading"
        assert loaded.category == FeedbackCategory.IMPROVEMENT.value
        assert loaded.status == FeedbackStatus.RESOLVED.value
