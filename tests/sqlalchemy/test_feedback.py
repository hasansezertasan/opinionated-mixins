from opinionated_mixins.contrib.sqlalchemy import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from sqlalchemy import Column, Index, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyFeedback(Feedback, Base):  # type: ignore[misc]
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyFeedback:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_defaults(self) -> None:
        with Session(self.engine) as session:
            obj = MyFeedback(subject="Bug report", content="Something broke")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.subject == "Bug report"
            assert obj.content == "Something broke"
            assert obj.category == FeedbackCategory.OTHER
            assert obj.status == FeedbackStatus.PENDING

    def test_create_with_explicit_values(self) -> None:
        with Session(self.engine) as session:
            obj = MyFeedback(
                subject="Feature idea",
                content="Add dark mode",
                category=FeedbackCategory.FEATURE,
                status=FeedbackStatus.REVIEWED,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.category == FeedbackCategory.FEATURE
            assert obj.status == FeedbackStatus.REVIEWED

    def test_no_default_indexes(self) -> None:
        table = MyFeedback.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert indexed_columns == set()

    def test_consumer_can_declare_indexes(self) -> None:
        class IndexedFeedback(Feedback, Base):  # type: ignore[misc]
            __tablename__ = "indexed_feedbacks"
            id = Column(Integer, primary_key=True)
            __table_args__ = (
                Index("ix_feedbacks_subject", "subject"),
                Index("ix_feedbacks_status", "status"),
            )

        table = IndexedFeedback.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert indexed_columns == {"subject", "status"}

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyFeedback.__table__.columns}
        assert {"subject", "content", "category", "status"}.issubset(columns)
