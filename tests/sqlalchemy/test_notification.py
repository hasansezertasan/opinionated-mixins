import datetime

from opinionated_mixins.contrib.sqlalchemy import Notification
from opinionated_mixins.enums import NotificationLevel
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyNotification(Notification, Base):  # type: ignore[misc]
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyNotification:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_required_fields(self) -> None:
        with Session(self.engine) as session:
            obj = MyNotification(
                notification_type="comment.reply",
                title="Someone replied",
                actor_type="User",
                actor_id="1",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.notification_type == "comment.reply"
            assert obj.title == "Someone replied"
            assert obj.level == NotificationLevel.INFO
            assert obj.actor_type == "User"
            assert obj.actor_id == "1"

    def test_create_with_all_fields(self) -> None:
        now = datetime.datetime.now(datetime.timezone.utc)
        with Session(self.engine) as session:
            obj = MyNotification(
                notification_type="order.shipped",
                level=NotificationLevel.SUCCESS,
                title="Order shipped",
                description="Your order is on the way",
                data={"order_id": "123"},
                actor_type="User",
                actor_id="42",
                action_url="https://example.com/orders/123",
                group_key="order.123",
                seen_at=now,
                read_at=now,
                archived_at=None,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.level == NotificationLevel.SUCCESS
            assert obj.actor_type == "User"
            assert obj.actor_id == "42"
            assert obj.group_key == "order.123"

    def test_created_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyNotification(
                notification_type="system.alert",
                title="Alert",
                actor_type="System",
                actor_id="system",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.created_at is not None

    def test_optional_fields_default_null(self) -> None:
        with Session(self.engine) as session:
            obj = MyNotification(
                notification_type="comment.reply",
                title="Reply",
                actor_type="User",
                actor_id="1",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.description is None
            assert obj.data is None
            assert obj.action_url is None
            assert obj.group_key is None
            assert obj.seen_at is None
            assert obj.read_at is None
            assert obj.archived_at is None

    def test_indexed_columns(self) -> None:
        table = MyNotification.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert "notification_type" in indexed_columns
        assert "level" in indexed_columns
        assert "group_key" in indexed_columns
        assert "seen_at" in indexed_columns
        assert "read_at" in indexed_columns
        assert "archived_at" in indexed_columns
        assert "created_at" in indexed_columns

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyNotification.__table__.columns}
        expected = {
            "notification_type",
            "level",
            "title",
            "description",
            "data",
            "actor_type",
            "actor_id",
            "action_url",
            "group_key",
            "seen_at",
            "read_at",
            "archived_at",
            "created_at",
        }
        assert expected.issubset(columns)
