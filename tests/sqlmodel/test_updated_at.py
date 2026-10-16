import datetime as dt

import pytest

from opinionated_mixins.contrib.sqlmodel import UpdatedAt, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyUpdatedAt(IntegerID, UpdatedAt, SQLModel, table=True):
    __tablename__ = "sqlmodel_updated_at"


class TestSQLModelUpdatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyUpdatedAt.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyUpdatedAt.model_fields)
        assert {"updated_at"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyUpdatedAt(updated_at=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc))
        assert obj.updated_at == dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)

    def test_defaults(self) -> None:
        obj = MyUpdatedAt()
        assert obj.updated_at.tzinfo is not None

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyUpdatedAt()
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyUpdatedAt)).one()
            assert loaded.id is not None

    @pytest.mark.parametrize("column", ["updated_at"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyUpdatedAt.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyUpdatedAt.__table__.indexes

    def test_onupdate_configured(self) -> None:
        assert MyUpdatedAt.__table__.c.updated_at.onupdate is not None
