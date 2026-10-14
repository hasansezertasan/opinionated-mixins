from opinionated_mixins.contrib.sqlmodel import Lead, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyLead(IntegerID, Lead, SQLModel, table=True):
    __tablename__ = "sqlmodel_lead"


class TestSQLModelLead:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyLead.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyLead.model_fields)
        assert {
            "status",
            "rating",
            "probability",
            "is_active",
            "opportunity_amount",
        } <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyLead(title="Acme")
        assert obj.title == "Acme"

    def test_defaults(self) -> None:
        obj = MyLead()
        assert obj.status is None
        assert obj.rating is None
        assert obj.probability == 0
        assert obj.is_active is True
        assert obj.opportunity_amount is None

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyLead()
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyLead)).one()
            assert loaded.id is not None

    def test_no_default_indexes(self) -> None:
        assert not MyLead.__table__.indexes
