# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.sqlalchemy import Announcement
from opinionated_mixins.enums import AnnouncementCategory
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyAnnouncement(Announcement, Base):  # type: ignore[misc]
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyAnnouncement:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_defaults(self) -> None:
        with Session(self.engine) as session:
            obj = MyAnnouncement(title="Test", content="Hello world")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.title == "Test"
            assert obj.content == "Hello world"
            assert obj.category == AnnouncementCategory.GENERAL

    def test_create_with_category(self) -> None:
        with Session(self.engine) as session:
            obj = MyAnnouncement(
                title="Downtime",
                content="Scheduled maintenance",
                category=AnnouncementCategory.MAINTENANCE,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.category == AnnouncementCategory.MAINTENANCE

    def test_title_indexed(self) -> None:
        table = MyAnnouncement.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert "title" in indexed_columns

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyAnnouncement.__table__.columns}
        assert {"title", "content", "category"}.issubset(columns)
