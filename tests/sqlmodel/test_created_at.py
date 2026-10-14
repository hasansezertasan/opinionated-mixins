import datetime

import pytest

from opinionated_mixins.contrib.sqlmodel import CreatedAt, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyCreatedAt(IntegerID, CreatedAt, SQLModel, table=True):
    __tablename__ = "sqlmodel_created_at"


class TestSQLModelCreatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyCreatedAt.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyCreatedAt.model_fields)
        assert {"created_at"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyCreatedAt(
            created_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)
        )
        assert obj.created_at == datetime.datetime(
            2024, 1, 1, tzinfo=datetime.timezone.utc
        )

    def test_defaults(self) -> None:
        obj = MyCreatedAt()
        assert obj.created_at.tzinfo is not None

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyCreatedAt()
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyCreatedAt)).one()
            assert loaded.id is not None

    @pytest.mark.parametrize("column", ["created_at"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyCreatedAt.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyCreatedAt.__table__.indexes
