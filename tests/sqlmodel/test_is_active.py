import pytest

from opinionated_mixins.contrib.sqlmodel import IsActive, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyIsActive(IntegerID, IsActive, SQLModel, table=True):
    __tablename__ = "sqlmodel_is_active"


class TestSQLModelIsActive:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyIsActive.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyIsActive.model_fields)
        assert {"is_active"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyIsActive(is_active=False)
        assert not obj.is_active

    def test_defaults(self) -> None:
        obj = MyIsActive()
        assert obj.is_active is True

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyIsActive()
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyIsActive)).one()
            assert loaded.id is not None

    @pytest.mark.parametrize("column", ["is_active"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyIsActive.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyIsActive.__table__.indexes
