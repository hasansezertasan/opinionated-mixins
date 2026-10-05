from opinionated_mixins.contrib.sqlalchemy import Template
from opinionated_mixins.enums import TemplateFormat, TemplateType
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyTemplate(Template, Base):  # type: ignore[misc]
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyTemplate:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_with_defaults(self) -> None:
        with Session(self.engine) as session:
            obj = MyTemplate(name="Welcome Email", content="Hello {{name}}")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.name == "Welcome Email"
            assert obj.content == "Hello {{name}}"
            assert obj.format == TemplateFormat.PLAIN
            assert obj.type == TemplateType.OTHER

    def test_create_with_explicit_values(self) -> None:
        with Session(self.engine) as session:
            obj = MyTemplate(
                name="Newsletter",
                content="<h1>News</h1>",
                format=TemplateFormat.HTML,
                type=TemplateType.EMAIL,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.format == TemplateFormat.HTML
            assert obj.type == TemplateType.EMAIL

    def test_name_indexed(self) -> None:
        table = MyTemplate.__table__
        indexed_columns = {col.name for idx in table.indexes for col in idx.columns}
        assert "name" in indexed_columns

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyTemplate.__table__.columns}
        assert {"name", "content", "format", "type"}.issubset(columns)
