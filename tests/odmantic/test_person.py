from opinionated_mixins.contrib.odmantic import Person


class TestODManticPerson:
    def test_has_expected_annotations(self) -> None:
        annotations = Person.__annotations__
        assert "first_name" in annotations
        assert "last_name" in annotations
        assert "middle_name" in annotations
        assert "phone_number" in annotations
        assert "email" in annotations
        assert "street_address" in annotations
        assert "postal_code" in annotations
        assert "city" in annotations
        assert "country" in annotations
        assert "date_of_birth" in annotations
        assert "bio" in annotations

    def test_optional_fields_default_none(self) -> None:
        for field_name in (
            "middle_name",
            "phone_number",
            "email",
            "street_address",
            "postal_code",
            "city",
            "country",
            "date_of_birth",
            "bio",
        ):
            field_info = getattr(Person, field_name).pydantic_field_info
            assert field_info.default is None, f"{field_name} should default to None"
