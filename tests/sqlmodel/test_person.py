import pytest

from opinionated_mixins.contrib.sqlmodel import Person, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyPerson(IntegerID, Person, SQLModel, table=True):
    __tablename__ = "sqlmodel_person"


class TestSQLModelPerson:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyPerson.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyPerson.model_fields)
        assert {
            "first_name",
            "last_name",
            "middle_name",
            "phone_number",
            "email",
            "street_address",
            "postal_code",
            "city",
            "country",
            "date_of_birth",
            "bio",
        } <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyPerson(first_name="Jane", last_name="Doe")
        assert obj.first_name == "Jane"
        assert obj.last_name == "Doe"

    def test_defaults(self) -> None:
        obj = MyPerson(first_name="Jane", last_name="Doe")
        assert obj.middle_name is None
        assert obj.phone_number is None
        assert obj.email is None
        assert obj.street_address is None
        assert obj.postal_code is None
        assert obj.city is None
        assert obj.country is None
        assert obj.date_of_birth is None
        assert obj.bio is None

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyPerson(first_name="Jane", last_name="Doe")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyPerson)).one()
            assert loaded.id is not None
            assert loaded.first_name == "Jane"
            assert loaded.last_name == "Doe"

    @pytest.mark.parametrize("column", ["first_name", "last_name"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyPerson.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyPerson.__table__.indexes
