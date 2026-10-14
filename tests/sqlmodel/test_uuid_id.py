import uuid

from opinionated_mixins.contrib.sqlmodel import UUIDID
from sqlmodel import Session, SQLModel, create_engine


class MyUUIDID(UUIDID, SQLModel, table=True):
    __tablename__ = "sqlmodel_uuid_id"


class TestSQLModelUUIDID:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyUUIDID.__table__])

    def test_id_is_primary_key(self) -> None:
        assert MyUUIDID.__table__.c.id.primary_key is True

    def test_id_generated_on_init(self) -> None:
        assert isinstance(MyUUIDID().id, uuid.UUID)

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyUUIDID()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert isinstance(obj.id, uuid.UUID)

    def test_ids_are_unique(self) -> None:
        assert MyUUIDID().id != MyUUIDID().id
