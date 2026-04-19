from opinionated_mixins.contrib.mongoengine import CreatedAt


class TestMongoEngineCreatedAt:
    def test_has_created_at_field(self) -> None:
        assert hasattr(CreatedAt, "created_at")

    def test_created_at_required(self) -> None:
        assert CreatedAt.created_at.required is True

    def test_created_at_has_default(self) -> None:
        assert CreatedAt.created_at.default is not None
