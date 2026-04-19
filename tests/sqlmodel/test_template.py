from opinionated_mixins.contrib.sqlmodel import Template


class TestSQLModelTemplate:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            Template as SATemplate,
        )

        assert Template is SATemplate
