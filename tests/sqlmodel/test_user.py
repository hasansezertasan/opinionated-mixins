import pytest

from opinionated_mixins.contrib.sqlmodel import User, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyUser(IntegerID, User, SQLModel, table=True):
    __tablename__ = "sqlmodel_user"


class TestSQLModelUser:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyUser.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyUser.model_fields)
        assert {"username", "hashed_password", "email", "date_email_verified"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyUser(username="janedoe", hashed_password="hashed123")
        assert obj.username == "janedoe"
        assert obj.hashed_password == "hashed123"  # pragma: allowlist secret

    def test_defaults(self) -> None:
        obj = MyUser(username="janedoe", hashed_password="hashed123")
        assert obj.email is None
        assert obj.date_email_verified is None

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyUser(username="janedoe", hashed_password="hashed123")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyUser)).one()
            assert loaded.id is not None
            assert loaded.username == "janedoe"
            assert loaded.hashed_password == "hashed123"  # pragma: allowlist secret

    @pytest.mark.parametrize("column", ["username", "hashed_password"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyUser.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyUser.__table__.indexes

    def test_assignment_is_allowed(self) -> None:
        obj = MyUser(username="janedoe", hashed_password="hashed123")
        obj.email = "jane@example.com"
        assert obj.email == "jane@example.com"

    @pytest.mark.parametrize("column", ["username", "email"])
    def test_unique_columns(self, column: str) -> None:
        assert MyUser.__table__.c[column].unique is True
