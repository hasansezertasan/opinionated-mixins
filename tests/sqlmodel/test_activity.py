import pytest

from opinionated_mixins.contrib.sqlmodel import Activity, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyActivity(IntegerID, Activity, SQLModel, table=True):
    __tablename__ = "sqlmodel_activity"


class TestSQLModelActivity:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyActivity.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyActivity.model_fields)
        assert {
            "verb",
            "actor_type",
            "actor_id",
            "description",
            "data",
            "target_type",
            "public",
        } <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyActivity(verb="created", actor_type="user", actor_id="1")
        assert obj.verb == "created"
        assert obj.actor_type == "user"
        assert obj.actor_id == "1"

    def test_defaults(self) -> None:
        obj = MyActivity(verb="created", actor_type="user", actor_id="1")
        assert obj.description is None
        assert obj.data is None
        assert obj.target_type is None
        assert obj.public is True

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(verb="created", actor_type="user", actor_id="1")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyActivity)).one()
            assert loaded.id is not None
            assert loaded.verb == "created"
            assert loaded.actor_type == "user"
            assert loaded.actor_id == "1"

    @pytest.mark.parametrize("column", ["verb", "actor_type", "actor_id"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyActivity.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyActivity.__table__.indexes

    def test_json_round_trip(self) -> None:
        payload = {"key": ["value", 1]}
        with Session(self.engine) as session:
            session.add(
                MyActivity(
                    verb="created", actor_type="user", actor_id="1", data=payload
                )
            )
            session.commit()
            assert session.exec(select(MyActivity)).one().data == payload
