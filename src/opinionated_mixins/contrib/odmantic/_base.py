"""Shared support for ODMantic mixins."""
# pyright: reportSelfClsParameterName=false

from typing import Any, cast
import warnings

from odmantic import Model

__all__ = ["ODManticMixinMetaclass"]

_ModelMetaclass = type(Model)


class ODManticMixinMetaclass(_ModelMetaclass):  # type: ignore[misc, valid-type]
    """Metaclass that makes plain mixin fields visible to ODMantic.

    ODMantic only inspects annotations present directly on the concrete model
    class namespace. When an opinionated mixin is composed with ``Model``, this
    metaclass copies annotated mixin fields into that namespace before ODMantic's
    own metaclass validates it.
    """

    def __new__(
        mcs,
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
                return cast(
                    "type",
                    super().__new__(  # pyright: ignore[reportUnknownMemberType]
                        mcs, name, bases, namespace, **kwargs
                    ),
                )
        return cast("type", type.__new__(cast("Any", mcs), name, bases, namespace))


def _has_odmantic_model_base(bases: tuple[type, ...]) -> bool:
    """Return whether any base participates in ODMantic model creation.

    Returns:
        Whether any base is an ODMantic model class.
    """
    return any(_is_odmantic_model_base(base) for base in bases)


def _is_odmantic_model_base(base: type) -> bool:
    """Return whether ``base`` is an ODMantic model class.

    Returns:
        Whether ``base`` subclasses ``odmantic.Model``.
    """
    try:
        return issubclass(base, Model)
    except TypeError:  # pragma: no cover - defensive for non-class bases
        return False


def _copy_mixin_fields(bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
    """Copy annotated fields from opinionated mixins into a model namespace."""
    annotations = _namespace_annotations(namespace)
    direct_field_names = set(annotations)
    for base in reversed(bases):
        if _is_odmantic_model_base(base):
            continue
        for mixin in reversed(base.__mro__):
            if mixin is object or _is_odmantic_model_base(mixin):
                continue
            _copy_fields_from_mixin(mixin, direct_field_names, annotations, namespace)
    namespace["__annotations__"] = annotations


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
    return dict(annotate(1))


def _copy_fields_from_mixin(
    mixin: type,
    direct_field_names: set[str],
    annotations: dict[str, Any],
    namespace: dict[str, Any],
) -> None:
    """Copy one mixin's annotations and defaults unless the model overrides them."""
    for field_name, annotation in getattr(mixin, "__annotations__", {}).items():
        annotations.setdefault(field_name, annotation)
        if (
            field_name not in direct_field_names
            and field_name not in namespace
            and hasattr(mixin, field_name)
        ):
            namespace[field_name] = getattr(mixin, field_name)
