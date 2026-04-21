from opinionated_mixins.contrib.mongoengine import Activity


class TestMongoEngineActivity:
    def test_has_verb_field(self) -> None:
        assert hasattr(Activity, "verb")
        assert Activity.verb.required is True
        assert Activity.verb.max_length == 255

    def test_has_description_field(self) -> None:
        assert hasattr(Activity, "description")
        assert Activity.description.required is False

    def test_has_data_field(self) -> None:
        assert hasattr(Activity, "data")

    def test_has_actor_fields(self) -> None:
        assert hasattr(Activity, "actor_type")
        assert Activity.actor_type.required is True
        assert Activity.actor_type.max_length == 255
        assert hasattr(Activity, "actor_id")
        assert Activity.actor_id.required is True
        assert Activity.actor_id.max_length == 255

    def test_has_target_fields(self) -> None:
        assert hasattr(Activity, "target_type")
        assert Activity.target_type.required is False
        assert Activity.target_type.max_length == 255
        assert hasattr(Activity, "target_id")
        assert Activity.target_id.required is False
        assert Activity.target_id.max_length == 255

    def test_has_action_object_fields(self) -> None:
        assert hasattr(Activity, "action_object_type")
        assert Activity.action_object_type.required is False
        assert Activity.action_object_type.max_length == 255
        assert hasattr(Activity, "action_object_id")
        assert Activity.action_object_id.required is False
        assert Activity.action_object_id.max_length == 255

    def test_has_public_field(self) -> None:
        assert hasattr(Activity, "public")
        assert Activity.public.required is True
        assert Activity.public.default is True

    def test_has_created_at_field(self) -> None:
        assert hasattr(Activity, "created_at")
        assert Activity.created_at.required is True
