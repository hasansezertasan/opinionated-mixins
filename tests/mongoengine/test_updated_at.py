from opinionated_mixins.contrib.mongoengine import UpdatedAt


class TestMongoEngineUpdatedAt:
    def test_has_updated_at_field(self) -> None:
        assert hasattr(UpdatedAt, "updated_at")

    def test_updated_at_required(self) -> None:
        assert UpdatedAt.updated_at.required is True

    def test_updated_at_has_default(self) -> None:
        assert UpdatedAt.updated_at.default is not None
