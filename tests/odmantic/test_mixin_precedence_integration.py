"""Integration tests for ODMantic mixin field precedence."""

from odmantic import Field, Model

from opinionated_mixins.contrib.odmantic._base import ODManticMixinMetaclass


class ParentMixin(metaclass=ODManticMixinMetaclass):
    """Parent mixin with an overridable field."""

    priority: int = Field(default=1)


class ChildMixin(ParentMixin):
    """Child mixin overriding a parent field."""

    priority: int = Field(default=2)


class LeftMixin(metaclass=ODManticMixinMetaclass):
    """Left mixin with a duplicate field."""

    flag: str = Field(default="left")


class RightMixin(metaclass=ODManticMixinMetaclass):
    """Right mixin with a duplicate field."""

    flag: str = Field(default="right")


class CommonMixin(metaclass=ODManticMixinMetaclass):
    """Common mixin with a field shared through a diamond."""

    status: str = Field(default="common")


class DiamondLeftMixin(CommonMixin):
    """Left diamond branch that inherits the common field."""


class DiamondRightMixin(CommonMixin):
    """Right diamond branch that overrides the common field."""

    status: str = Field(default="right")


class TestODManticMixinPrecedence:
    """Test that copied mixin fields follow Python MRO precedence."""

    def test_leftmost_mixin_wins_duplicate_field(self) -> None:
        class MyModel(LeftMixin, RightMixin, Model):
            model_config = {"collection": "test_mixin_precedence_leftmost"}

        obj = MyModel()
        assert obj.flag == "left"

    def test_child_mixin_wins_parent_duplicate_field(self) -> None:
        class MyModel(ChildMixin, Model):
            model_config = {"collection": "test_mixin_precedence_child"}

        obj = MyModel()
        assert obj.priority == 2

    def test_c3_mro_wins_diamond_duplicate_field(self) -> None:
        class MyModel(DiamondLeftMixin, DiamondRightMixin, Model):
            model_config = {"collection": "test_mixin_precedence_diamond"}

        obj = MyModel()
        assert obj.status == "right"
