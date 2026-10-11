"""Guard the TYPE_CHECKING ``Mapped[...]`` annotations against Column drift.

SQLAlchemy mixins declare each field twice (RFC-0015): a ``Mapped[...]``
annotation that only type checkers see, and the runtime ``Column(...)``. These
tests parse the annotations from source and check that they agree with the
columns on name, nullability, and Python type.
"""

from __future__ import annotations

import ast
import datetime
import decimal
import inspect
import sys
import types
import uuid
from typing import Any, Union, get_args, get_origin

import pytest
from opinionated_mixins.contrib import sqlalchemy as sa_contrib
from sqlalchemy import Column
from sqlalchemy.orm import Mapped

MIXINS = [
    getattr(sa_contrib, name) for name in sorted(dir(sa_contrib)) if name[0].isupper()
]


def _is_type_checking(node: ast.stmt) -> bool:
    return isinstance(node, ast.If) and ast.unparse(node.test) == "TYPE_CHECKING"


def _annotations(mixin: type) -> dict[str, object]:
    """Evaluate the mixin's TYPE_CHECKING annotations into ``Mapped[...]`` args."""
    tree = ast.parse(inspect.getsource(mixin))
    class_def = tree.body[0]
    assert isinstance(class_def, ast.ClassDef)
    blocks = [node for node in class_def.body if _is_type_checking(node)]
    assert len(blocks) == 1, f"{mixin.__name__} needs one TYPE_CHECKING block"
    namespace: dict[str, Any] = {
        **vars(sys.modules[mixin.__module__]),
        "Any": Any,
        "Decimal": decimal.Decimal,
        "Mapped": Mapped,
        "datetime": datetime,
        "uuid": uuid,
    }
    result: dict[str, object] = {}
    for stmt in blocks[0].body:
        assert isinstance(stmt, ast.AnnAssign), ast.unparse(stmt)
        assert isinstance(stmt.target, ast.Name)
        annotation = eval(ast.unparse(stmt.annotation), namespace)  # noqa: S307
        assert get_origin(annotation) is Mapped, ast.unparse(stmt)
        (result[stmt.target.id],) = get_args(annotation)
    return result


def _columns(mixin: type) -> dict[str, Column[Any]]:
    return {
        name: value for name, value in vars(mixin).items() if isinstance(value, Column)
    }


def _split_optional(annotation: object) -> tuple[object, bool]:
    if get_origin(annotation) not in {Union, types.UnionType}:
        return annotation, False
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    assert len(args) == 1, annotation
    return args[0], len(args) != len(get_args(annotation))


@pytest.mark.parametrize("mixin", MIXINS, ids=lambda m: m.__name__)
def test_annotations_match_column_names(mixin: type) -> None:
    assert set(_annotations(mixin)) == set(_columns(mixin))


@pytest.mark.parametrize("mixin", MIXINS, ids=lambda m: m.__name__)
def test_annotations_match_column_nullability(mixin: type) -> None:
    columns = _columns(mixin)
    for name, annotation in _annotations(mixin).items():
        _, optional = _split_optional(annotation)
        assert optional is bool(columns[name].nullable), name


@pytest.mark.parametrize("mixin", MIXINS, ids=lambda m: m.__name__)
def test_annotations_match_column_python_type(mixin: type) -> None:
    columns = _columns(mixin)
    for name, annotation in _annotations(mixin).items():
        inner, _ = _split_optional(annotation)
        python_type = get_origin(inner) or inner
        assert python_type is columns[name].type.python_type, name
