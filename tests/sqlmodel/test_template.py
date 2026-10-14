import pytest

from opinionated_mixins.enums import TemplateFormat, TemplateType
from opinionated_mixins.contrib.sqlmodel import Template, IntegerID
from sqlmodel import Session, SQLModel, create_engine, select


class MyTemplate(IntegerID, Template, SQLModel, table=True):
    __tablename__ = "sqlmodel_template"


class TestSQLModelTemplate:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine, tables=[MyTemplate.__table__])

    def test_native_pydantic_fields(self) -> None:
        """Mixin columns are model fields, not just schema (issue #167)."""
        names = set(MyTemplate.model_fields)
        assert {"name", "content", "format", "type"} <= names

    def test_constructor_keeps_values(self) -> None:
        obj = MyTemplate(name="N", content="C")
        assert obj.name == "N"
        assert obj.content == "C"

    def test_defaults(self) -> None:
        obj = MyTemplate(name="N", content="C")
        assert obj.format == TemplateFormat.PLAIN
        assert obj.type == TemplateType.OTHER

    def test_round_trip(self) -> None:
        with Session(self.engine) as session:
            obj = MyTemplate(name="N", content="C")
            session.add(obj)
            session.commit()
            loaded = session.exec(select(MyTemplate)).one()
            assert loaded.id is not None
            assert loaded.name == "N"
            assert loaded.content == "C"

    @pytest.mark.parametrize("column", ["name", "content"])
    def test_required_columns_not_nullable(self, column: str) -> None:
        assert MyTemplate.__table__.c[column].nullable is False

    def test_no_default_indexes(self) -> None:
        assert not MyTemplate.__table__.indexes
