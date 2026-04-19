import datetime

from opinionated_mixins.contrib.sqlalchemy import User
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyUser(User, Base):  # type: ignore[misc]
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyUser:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_required_only(self) -> None:
        with Session(self.engine) as session:
            obj = MyUser(username="janedoe", hashed_password="hashed123")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.username == "janedoe"
            assert obj.hashed_password == "hashed123"
            assert obj.email is None
            assert obj.date_email_verified is None

    def test_create_with_all_fields(self) -> None:
        with Session(self.engine) as session:
            now = datetime.datetime(2024, 1, 15, 12, 0, 0)
            obj = MyUser(
                username="janedoe",
                hashed_password="hashed123",
                email="jane@example.com",
                date_email_verified=now,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.email == "jane@example.com"
            assert obj.date_email_verified == now

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyUser.__table__.columns}
        expected = {
            "username",
            "hashed_password",
            "email",
            "date_email_verified",
        }
        assert expected.issubset(columns)

    def test_username_unique_constraint(self) -> None:
        col = MyUser.__table__.c.username
        assert col.unique is True

    def test_username_index(self) -> None:
        col = MyUser.__table__.c.username
        assert col.index is True

    def test_email_unique_constraint(self) -> None:
        col = MyUser.__table__.c.email
        assert col.unique is True

    def test_email_index(self) -> None:
        col = MyUser.__table__.c.email
        assert col.index is True
