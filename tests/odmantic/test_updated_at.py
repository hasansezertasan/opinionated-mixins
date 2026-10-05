from opinionated_mixins.contrib.odmantic import UpdatedAt


class TestODManticUpdatedAt:
    def test_has_expected_annotations(self) -> None:
        annotations = UpdatedAt.__annotations__
        assert "updated_at" in annotations

    def test_updated_at_has_default(self) -> None:
        field_info = UpdatedAt.updated_at.pydantic_field_info
        assert field_info.default_factory is not None
