import datetime

from opinionated_mixins.contrib.sqlalchemy import CreatedAt
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(CreatedAt, Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyCreatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_created_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.created_at is not None
            assert isinstance(obj.created_at, datetime.datetime)

    def test_created_at_not_null(self) -> None:
        col = MyModel.__table__.c.created_at
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "created_at" in columns
