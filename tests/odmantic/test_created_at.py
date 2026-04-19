from opinionated_mixins.contrib.odmantic import CreatedAt


class TestODManticCreatedAt:
    def test_has_expected_annotations(self) -> None:
        annotations = CreatedAt.__annotations__
        assert "created_at" in annotations

    def test_created_at_has_default(self) -> None:
        field_info = CreatedAt.created_at.pydantic_field_info
        assert field_info.default_factory is not None
