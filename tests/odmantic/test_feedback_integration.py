"""Integration tests for ODMantic Feedback mixin."""

import pytest
from odmantic import Model
from opinionated_mixins.contrib.odmantic import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus

pytestmark = pytest.mark.xfail(
    reason="ODMantic metaclass does not process annotations from mixin parents. "
    "See: https://github.com/hasansezertasan/opinionated-mixins/issues/39",
    strict=True,
)


class MyFeedback(Feedback, Model):
    """Test model composing Feedback with Model."""

    model_config = {"collection": "test_feedbacks"}


class TestFeedbackIntegration:
    """Test Feedback mixin composition, instantiation, and roundtrip."""

    async def test_create_with_defaults(self, mock_engine) -> None:
        obj = MyFeedback(subject="Bug report", content="Something broke")
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyFeedback)
        assert loaded is not None
        assert loaded.subject == "Bug report"
        assert loaded.content == "Something broke"
        assert loaded.category == FeedbackCategory.OTHER
        assert loaded.status == FeedbackStatus.PENDING

    async def test_create_with_explicit_values(self, mock_engine) -> None:
        obj = MyFeedback(
            subject="Feature request",
            content="Add dark mode",
            category=FeedbackCategory.FEATURE,
            status=FeedbackStatus.REVIEWED,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyFeedback)
        assert loaded.category == FeedbackCategory.FEATURE
        assert loaded.status == FeedbackStatus.REVIEWED

    async def test_roundtrip_preserves_all_fields(self, mock_engine) -> None:
        obj = MyFeedback(
            subject="Improvement",
            content="Faster loading",
            category=FeedbackCategory.IMPROVEMENT,
            status=FeedbackStatus.RESOLVED,
        )
        await mock_engine.save(obj)
        loaded = await mock_engine.find_one(MyFeedback)
        assert loaded.subject == "Improvement"
        assert loaded.content == "Faster loading"
        assert loaded.category == FeedbackCategory.IMPROVEMENT
        assert loaded.status == FeedbackStatus.RESOLVED
