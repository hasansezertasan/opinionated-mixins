import pytest

from opinionated_mixins.enums import FeedbackCategory, FeedbackStatus
from opinionated_mixins.contrib.sqlmodel import Feedback, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyFeedback(IntegerID, Feedback, SQLModel, table=True):
    __tablename__ = "sqlmodel_feedback"


class TestSQLModelFeedback:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyFeedback.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyFeedback.model_fields)
        assert {"subject", "content", "category", "status"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyFeedback(subject="S", content="C")
        assert obj.subject == "S"
        assert obj.content == "C"

    def test_defaults(self) -> None:
        obj = MyFeedback(subject="S", content="C")
        assert obj.category == FeedbackCategory.OTHER
        assert obj.status == FeedbackStatus.PENDING

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyFeedback(subject="S", content="C")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyFeedback)).one()
            assert loaded.id is not None
            assert loaded.subject == "S"
            assert loaded.content == "C"

    @pytest.mark.parametrize("column", ["subject", "content"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyFeedback.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyFeedback.__table__.indexes
