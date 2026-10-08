"""Integration tests for ODMantic mixin field precedence."""

import sys

from odmantic import Field, Model
import pytest
from pydantic import ValidationError

from opinionated_mixins.contrib.odmantic._base import (
    ODManticMixinMetaclass,
    _class_annotations,
    _mro_for_bases,
    _namespace_annotations,
)


class ParentMixin(metaclass=ODManticMixinMetaclass):
    """Parent mixin with an overridable field."""

    priority: int = Field(default=1)


class ChildMixin(ParentMixin):
    """Child mixin overriding a parent field."""

    priority: int = Field(default=2)


class RequiredChildMixin(ParentMixin):
    """Child mixin making a parent field required."""

    priority: int


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

    def test_child_annotation_overrides_parent_default(self) -> None:
        class MyModel(RequiredChildMixin, Model):
            model_config = {"collection": "test_mixin_precedence_required_child"}

        with pytest.raises(ValidationError):
            MyModel()

        obj = MyModel(priority=3)
        assert obj.priority == 3

    def test_c3_mro_wins_diamond_duplicate_field(self) -> None:
        class MyModel(DiamondLeftMixin, DiamondRightMixin, Model):
            model_config = {"collection": "test_mixin_precedence_diamond"}

        obj = MyModel()
        assert obj.status == "right"

    def test_inconsistent_mixin_mro_is_rejected(self) -> None:
        class LeftFirstMixin(LeftMixin, RightMixin):
            pass

        class RightFirstMixin(RightMixin, LeftMixin):
            pass

        with pytest.raises(TypeError, match="consistent method resolution order"):
            _mro_for_bases((LeftFirstMixin, RightFirstMixin, Model))

    def test_unrelated_annotated_base_is_not_persisted(self) -> None:
        class CacheBase:
            timeout: int = 30

        class MyModel(LeftMixin, CacheBase, Model):
            pass

        obj = MyModel()

        assert obj.timeout == 30
        assert "timeout" not in MyModel.__odm_fields__
        assert "timeout" not in obj.model_dump_doc()

    @pytest.mark.skipif(
        sys.version_info < (3, 14), reason="native lazy annotations require Python 3.14"
    )
    def test_lazy_annotations_preserve_forward_references(self) -> None:
        class MyModel:
            related: NotYetDefined  # noqa: F821

        namespace = {"__annotate_func__": MyModel.__annotate_func__}

        annotations = _namespace_annotations(namespace)

        assert set(annotations) == {"related"}

    @pytest.mark.skipif(
        sys.version_info < (3, 14), reason="native lazy annotations require Python 3.14"
    )
    def test_lazy_mixin_annotations_preserve_forward_references(self) -> None:
        class RelatedMixin(metaclass=ODManticMixinMetaclass):
            related: NotYetDefined  # noqa: F821

        annotations = _class_annotations(RelatedMixin)

        assert set(annotations) == {"related"}
