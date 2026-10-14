import pytest

from opinionated_mixins.enums import AnnouncementCategory
from opinionated_mixins.contrib.sqlmodel import Announcement, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyAnnouncement(IntegerID, Announcement, SQLModel, table=True):
    __tablename__ = "sqlmodel_announcement"


class TestSQLModelAnnouncement:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyAnnouncement.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyAnnouncement.model_fields)
        assert {"title", "content", "category"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyAnnouncement(title="T", content="C")
        assert obj.title == "T"
        assert obj.content == "C"

    def test_defaults(self) -> None:
        obj = MyAnnouncement(title="T", content="C")
        assert obj.category == AnnouncementCategory.GENERAL

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyAnnouncement(title="T", content="C")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyAnnouncement)).one()
            assert loaded.id is not None
            assert loaded.title == "T"
            assert loaded.content == "C"

    @pytest.mark.parametrize("column", ["title", "content"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyAnnouncement.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyAnnouncement.__table__.indexes
