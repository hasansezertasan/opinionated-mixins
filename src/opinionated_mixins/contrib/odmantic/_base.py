"""Shared support for ODMantic mixins."""
# pyright: reportSelfClsParameterName=false

import datetime
from collections.abc import Callable
from decimal import Decimal
from typing import Annotated, Any, cast, get_args, get_origin
import importlib
import types
import typing
import warnings

from bson.decimal128 import Decimal128
from odmantic import EmbeddedModel, Model
from odmantic.field import ODMField

__all__ = ["ODManticMixinMetaclass"]

_ModelMetaclass = type(Model)
_EmbeddedModelMetaclass = type(EmbeddedModel)


def date_to_datetime_for_bson(value: object) -> object:
    """Return a BSON-compatible datetime for date-only values.

    Returns:
        A midnight datetime for date-only values, otherwise the original value.
    """
    if value is None or isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime.combine(value, datetime.time())
    return value


def decimal_to_decimal128_for_bson(value: object) -> object:
    """Return a BSON-compatible Decimal128 for decimal values.

    Returns:
        A BSON Decimal128 for Decimal values, otherwise the original value.
    """
    if isinstance(value, Decimal):
        return Decimal128(value)
    return value


def bson_key_for_field(model: type, field_name: str) -> str:
    """Return the BSON document key for an ODMantic field.

    Returns:
        The field key name used in document dumps.
    """
    odm_field = cast("Any", model).__odm_fields__[field_name]
    return cast("str", odm_field.key_name)


def utc_datetime(value: object) -> object:
    """Return UTC-aware datetimes for decoded BSON values.

    Returns:
        A UTC-aware datetime for datetime values, otherwise the original value.
    """
    if not isinstance(value, datetime.datetime):
        return value
    if value.tzinfo is None:
        return value.replace(tzinfo=datetime.timezone.utc)
    return value.astimezone(datetime.timezone.utc)


class ODManticMixinMetaclass(_EmbeddedModelMetaclass, _ModelMetaclass):  # type: ignore[misc, valid-type]
    """Metaclass that makes plain mixin fields visible to ODMantic.

    ODMantic only inspects annotations present directly on the concrete model
    class namespace. When an opinionated mixin is composed with ``Model``, this
    metaclass copies annotated mixin fields into that namespace before ODMantic's
    own metaclass validates it.
    """

    def __new__(  # pylint: disable=bad-mcs-classmethod-argument
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: object,
    ) -> type:
        """Create mixin classes normally and hydrate ODMantic model subclasses."""
        if _has_odmantic_model_base(bases):
            _copy_mixin_fields(bases, namespace)
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message=r'Field name ".*" in ".*" shadows an attribute in parent',
                    category=UserWarning,
                )
                return _create_odmantic_class(cls, name, bases, namespace, kwargs)
        return cast("type", type.__new__(cast("Any", cls), name, bases, namespace))


def _create_odmantic_class(
    metaclass: type,
    name: str,
    bases: tuple[type, ...],
    namespace: dict[str, Any],
    kwargs: dict[str, object],
) -> type:
    """Dispatch to collection or embedded model creation without sibling validation.

    Returns:
        The concrete ODMantic model class.

    Raises:
        TypeError: If an embedded model declares a primary field.
    """
    if any(issubclass(base, Model) for base in bases):
        creator = super(cast("Any", _EmbeddedModelMetaclass), cast("Any", metaclass))
    else:
        # EmbeddedModelMetaclass's super() would also run ModelMetaclass in this
        # combined MRO, incorrectly adding a primary key and collection metadata.
        cast("Any", metaclass).__validate_cls_namespace__(name, namespace)
        for field in namespace["__odm_fields__"].values():
            if isinstance(field, ODMField) and field.primary_field:
                msg = f"cannot define a primary field in {name} embedded document"
                raise TypeError(msg)
        creator = super(cast("Any", _ModelMetaclass), cast("Any", metaclass))
    model = cast(
        "type",
        cast("Any", creator).__new__(metaclass, name, bases, namespace, **kwargs),
    )
    _register_bson_serializers(model)
    return model


def _register_bson_serializers(model: type) -> None:
    """Register BSON conversions for nested documents as well as top-level dumps."""
    for field_name, field in cast("Any", model).model_fields.items():
        serializer = _bson_serializer_for_annotation(field.annotation)
        if serializer is not None:
            cast("Any", model).__bson_serializers__.setdefault(field_name, serializer)


def _bson_serializer_for_annotation(
    annotation: object,
) -> Callable[[object], object] | None:
    """Find a date or decimal converter through optional and annotated types.

    Returns:
        A BSON converter, or None for fields that do not need conversion.
    """
    if annotation is datetime.date:
        return date_to_datetime_for_bson
    if annotation is Decimal:
        return decimal_to_decimal128_for_bson
    for argument in _scalar_annotation_arguments(annotation):
        serializer = _bson_serializer_for_annotation(argument)
        if serializer is not None:
            return serializer
    return None


def _scalar_annotation_arguments(annotation: object) -> tuple[Any, ...]:
    """Unwrap scalar annotation metadata and unions, but leave containers alone.

    Returns:
        Inner scalar annotations, or an empty tuple for other types.
    """
    if get_origin(annotation) is Annotated:
        return get_args(annotation)[:1]
    # ODMantic uses both legacy typing unions and PEP 604 unions at runtime.
    if get_origin(annotation) in {typing.Union, types.UnionType}:  # pyright: ignore[reportDeprecated]
        return get_args(annotation)
    return ()


def _has_odmantic_model_base(bases: tuple[type, ...]) -> bool:
    """Return whether any base participates in ODMantic model creation.

    Returns:
        Whether any base is an ODMantic model class.
    """
    return any(_is_odmantic_model_base(base) for base in bases)


def _is_odmantic_model_base(base: type) -> bool:
    """Return whether ``base`` is an ODMantic model class.

    Returns:
        Whether ``base`` subclasses ``odmantic.Model`` or ``EmbeddedModel``.
    """
    try:
        return issubclass(base, (Model, EmbeddedModel))
    except TypeError:  # pragma: no cover - defensive for non-class bases
        return False


def _copy_mixin_fields(bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
    """Copy annotated fields from opinionated mixins into a model namespace."""
    annotations = _namespace_annotations(namespace)
    copied_field_names = set(annotations)
    for mixin in _mro_for_bases(bases):
        if not isinstance(cast("Any", mixin), ODManticMixinMetaclass):
            continue
        _copy_fields_from_mixin(mixin, copied_field_names, annotations, namespace)
    namespace["__annotations__"] = annotations


def _mro_for_bases(bases: tuple[type, ...]) -> list[type]:
    """Return non-model bases in Python C3 MRO order.

    Returns:
        MRO sequence for non-ODMantic-model bases, excluding the new class itself.
    """
    base_list = [base for base in bases if not _is_odmantic_model_base(base)]
    seqs = [list(base.__mro__) for base in base_list]
    seqs.append(base_list.copy())
    return _merge_mro(seqs)


def _merge_mro(seqs: list[list[type]]) -> list[type]:
    """Merge MRO candidate sequences using Python's C3 linearization.

    Returns:
        The merged MRO sequence.
    """
    result: list[type] = []
    while True:
        seqs = [seq for seq in seqs if seq]
        if not seqs:
            return result
        candidate = _next_mro_candidate(seqs)
        result.append(candidate)
        for seq in seqs:
            if seq[0] is candidate:
                _ = seq.pop(0)


def _next_mro_candidate(seqs: list[list[type]]) -> type:
    """Return the next valid C3 MRO candidate.

    Returns:
        The next class that does not appear in any sequence tail.

    Raises:
        TypeError: If the base classes do not have a consistent MRO.
    """
    for seq in seqs:
        candidate = seq[0]
        if not any(candidate in other_seq[1:] for other_seq in seqs):
            return candidate
    msg = "Cannot create a consistent method resolution order"
    raise TypeError(msg)


def _namespace_annotations(namespace: dict[str, Any]) -> dict[str, Any]:
    """Return direct class annotations, including Python 3.14 lazy annotations.

    Returns:
        Direct class annotations resolved from eager or lazy annotation storage.
    """
    annotations = namespace.get("__annotations__")
    if annotations is not None:
        return dict(annotations)
    annotate = namespace.get("__annotate_func__")
    if annotate is None:
        return {}
    try:
        annotationlib = importlib.import_module("annotationlib")
    except ModuleNotFoundError:  # pragma: no cover - Python < 3.14 fallback.
        return dict(annotate(1))
    return dict(
        annotationlib.call_annotate_function(annotate, annotationlib.Format.FORWARDREF)
    )


def _class_annotations(cls: type) -> dict[str, Any]:
    """Return class annotations without forcing Python 3.14 value resolution.

    Returns:
        Class annotations resolved from eager or lazy annotation storage.
    """
    annotations = vars(cls).get("__annotations__")
    if annotations is not None:
        return dict(annotations)
    annotate = vars(cls).get("__annotate_func__")
    if annotate is None:
        return {}
    try:
        annotationlib = importlib.import_module("annotationlib")
    except ModuleNotFoundError:  # pragma: no cover - Python < 3.14 fallback.
        return dict(annotate(1))
    return dict(
        annotationlib.call_annotate_function(annotate, annotationlib.Format.FORWARDREF)
    )


def _copy_fields_from_mixin(
    mixin: type,
    copied_field_names: set[str],
    annotations: dict[str, Any],
    namespace: dict[str, Any],
) -> None:
    """Copy one mixin's annotations and defaults unless the model overrides them."""
    declared_defaults = mixin.__dict__
    for field_name, annotation in _class_annotations(mixin).items():
        annotations.setdefault(field_name, annotation)
        if field_name in copied_field_names:
            continue
        copied_field_names.add(field_name)
        if field_name not in namespace and field_name in declared_defaults:
            namespace[field_name] = declared_defaults[field_name]
