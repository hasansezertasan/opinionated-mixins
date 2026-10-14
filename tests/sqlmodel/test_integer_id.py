from opinionated_mixins.contrib.sqlmodel import IntegerID
from sqlmodel import Session, SQLModel, create_engine


class MyIntegerID(IntegerID, SQLModel, table=True):
    __tablename__ = "sqlmodel_integer_id"


class TestSQLModelIntegerID:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyIntegerID.__table__])

    def test_id_is_primary_key(self) -> None:
        assert MyIntegerID.__table__.c.id.primary_key is True

    def test_id_none_until_flushed(self) -> None:
        assert MyIntegerID().id is None

    def test_autoincrement(self) -> None:
        with Session(self.engine) as session:
            first, second = MyIntegerID(), MyIntegerID()
            session.add_all([first, second])
            session.commit()
            assert (first.id, second.id) == (1, 2)
