from opinionated_mixins.contrib.sqlalchemy import IsActive
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(IsActive, Base):  # type: ignore[misc]
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyIsActive:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_is_active_defaults_true(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.is_active is True

    def test_is_active_can_be_set_false(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel(is_active=False)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.is_active is False

    def test_is_active_not_null(self) -> None:
        col = MyModel.__table__.c.is_active
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "is_active" in columns
