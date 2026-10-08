from opinionated_mixins.contrib.sqlalchemy import IsActive
from sqlalchemy import Column, Index, Integer, create_engine
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

    def test_no_default_indexes(self) -> None:
        table = MyModel.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert indexed_columns == set()

    def test_consumer_can_declare_indexes(self) -> None:
        class IndexedModel(IsActive, Base):  # type: ignore[misc]
            __tablename__ = "indexed_items_is_active"
            id = Column(Integer, primary_key=True)
            __table_args__ = (Index("ix_items_is_active", "is_active"),)

        table = IndexedModel.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert indexed_columns == {"is_active"}
