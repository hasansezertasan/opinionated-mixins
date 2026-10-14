import pytest

from opinionated_mixins.enums import NotificationLevel
from opinionated_mixins.contrib.sqlmodel import Notification, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyNotification(IntegerID, Notification, SQLModel, table=True):
    __tablename__ = "sqlmodel_notification"


class TestSQLModelNotification:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyNotification.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyNotification.model_fields)
        assert {
            "notification_type",
            "title",
            "actor_type",
            "actor_id",
            "description",
            "data",
            "seen_at",
            "read_at",
            "archived_at",
            "level",
        } <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyNotification(
            notification_type="order.shipped",
            title="Shipped",
            actor_type="user",
            actor_id="1",
        )
        assert obj.notification_type == "order.shipped"
        assert obj.title == "Shipped"
        assert obj.actor_type == "user"
        assert obj.actor_id == "1"

    def test_defaults(self) -> None:
        obj = MyNotification(
            notification_type="order.shipped",
            title="Shipped",
            actor_type="user",
            actor_id="1",
        )
        assert obj.description is None
        assert obj.data is None
        assert obj.seen_at is None
        assert obj.read_at is None
        assert obj.archived_at is None
        assert obj.level == NotificationLevel.INFO

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyNotification(
                notification_type="order.shipped",
                title="Shipped",
                actor_type="user",
                actor_id="1",
            )
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyNotification)).one()
            assert loaded.id is not None
            assert loaded.notification_type == "order.shipped"
            assert loaded.title == "Shipped"
            assert loaded.actor_type == "user"
            assert loaded.actor_id == "1"

    @pytest.mark.parametrize(
        "column", ["notification_type", "title", "actor_type", "actor_id"]
    )
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyNotification.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyNotification.__table__.indexes
