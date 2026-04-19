import datetime

from opinionated_mixins.contrib.sqlalchemy import UpdatedAt
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(UpdatedAt, Base):  # type: ignore[misc]
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)


class TestSQLAlchemyUpdatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_updated_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.updated_at is not None
            assert isinstance(obj.updated_at, datetime.datetime)

    def test_updated_at_changes_on_update(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel(name="original")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            original_updated = obj.updated_at

            obj.name = "modified"
            session.commit()
            session.refresh(obj)
            assert obj.updated_at >= original_updated

    def test_updated_at_not_null(self) -> None:
        col = MyModel.__table__.c.updated_at
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "updated_at" in columns
