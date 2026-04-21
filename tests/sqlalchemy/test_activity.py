import datetime

from opinionated_mixins.contrib.sqlalchemy import Activity
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyActivity(Activity, Base):  # type: ignore[misc]
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyActivity:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_required_fields(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(
                verb="commented",
                actor_type="User",
                actor_id="42",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.verb == "commented"
            assert obj.actor_type == "User"
            assert obj.actor_id == "42"
            assert obj.public is True

    def test_create_with_all_fields(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(
                verb="commented",
                description="Alice commented on a pull request",
                data={"comment_id": "5"},
                actor_type="User",
                actor_id="42",
                target_type="PullRequest",
                target_id="99",
                action_object_type="Comment",
                action_object_id="5",
                public=False,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.verb == "commented"
            assert obj.description == "Alice commented on a pull request"
            assert obj.data == {"comment_id": "5"}
            assert obj.actor_type == "User"
            assert obj.actor_id == "42"
            assert obj.target_type == "PullRequest"
            assert obj.target_id == "99"
            assert obj.action_object_type == "Comment"
            assert obj.action_object_id == "5"
            assert obj.public is False

    def test_created_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(
                verb="merged",
                actor_type="User",
                actor_id="1",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.created_at is not None
            assert isinstance(obj.created_at, datetime.datetime)

    def test_optional_fields_default_null(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(
                verb="deployed",
                actor_type="System",
                actor_id="system",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.description is None
            assert obj.data is None
            assert obj.target_type is None
            assert obj.target_id is None
            assert obj.action_object_type is None
            assert obj.action_object_id is None

    def test_public_defaults_true(self) -> None:
        with Session(self.engine) as session:
            obj = MyActivity(
                verb="created",
                actor_type="User",
                actor_id="1",
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.public is True

    def test_indexed_columns(self) -> None:
        table = MyActivity.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert "verb" in indexed_columns
        assert "actor_type" in indexed_columns
        assert "actor_id" in indexed_columns
        assert "target_type" in indexed_columns
        assert "target_id" in indexed_columns
        assert "action_object_type" in indexed_columns
        assert "action_object_id" in indexed_columns
        assert "public" in indexed_columns
        assert "created_at" in indexed_columns

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyActivity.__table__.columns}
        expected = {
            "verb",
            "description",
            "data",
            "actor_type",
            "actor_id",
            "target_type",
            "target_id",
            "action_object_type",
            "action_object_id",
            "public",
            "created_at",
        }
        assert expected.issubset(columns)
