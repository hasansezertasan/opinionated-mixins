from opinionated_mixins.contrib.mongoengine import IsActive


class TestMongoEngineIsActive:
    def test_has_is_active_field(self) -> None:
        assert hasattr(IsActive, "is_active")

    def test_is_active_required(self) -> None:
        assert IsActive.is_active.required is True

    def test_is_active_defaults_true(self) -> None:
        assert IsActive.is_active.default is True
