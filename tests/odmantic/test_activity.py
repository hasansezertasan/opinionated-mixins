from opinionated_mixins.contrib.odmantic import Activity


class TestODManticActivity:
    def test_has_expected_annotations(self) -> None:
        annotations = Activity.__annotations__
        assert "verb" in annotations
        assert "description" in annotations
        assert "data" in annotations
        assert "actor_type" in annotations
        assert "actor_id" in annotations
        assert "target_type" in annotations
        assert "target_id" in annotations
        assert "action_object_type" in annotations
        assert "action_object_id" in annotations
        assert "public" in annotations
        assert "created_at" in annotations

    def test_public_default(self) -> None:
        assert Activity.public.pydantic_field_info.default is True
