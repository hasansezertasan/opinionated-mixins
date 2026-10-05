from opinionated_mixins.contrib.sqlalchemy import Feedback
from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from sqlalchemy import Column, Integer, create_engine
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

    def test_subject_indexed(self) -> None:
        table = MyFeedback.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert "subject" in indexed_columns

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyFeedback.__table__.columns}
        assert {"subject", "content", "category", "status"}.issubset(columns)
