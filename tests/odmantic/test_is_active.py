from opinionated_mixins.contrib.odmantic import IsActive


class TestODManticIsActive:
    def test_has_expected_annotations(self) -> None:
        annotations = IsActive.__annotations__
        assert "is_active" in annotations

    def test_is_active_defaults_true(self) -> None:
        field_info = IsActive.is_active.pydantic_field_info
        assert field_info.default is True
