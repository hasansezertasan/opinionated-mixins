from opinionated_mixins.contrib.sqlalchemy import IntegerID
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(IntegerID, Base):  # type: ignore[misc]
    __tablename__ = "items"


class TestSQLAlchemyIntegerID:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_id_is_primary_key(self) -> None:
        col = MyModel.__table__.c.id
        assert col.primary_key is True

    def test_id_auto_increments(self) -> None:
        with Session(self.engine) as session:
            obj1 = MyModel()
            obj2 = MyModel()
            session.add_all([obj1, obj2])
            session.commit()
            session.refresh(obj1)
            session.refresh(obj2)
            assert obj1.id == 1
            assert obj2.id == 2

    def test_id_is_integer(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert isinstance(obj.id, int)

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "id" in columns
