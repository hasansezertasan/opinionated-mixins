from opinionated_mixins.contrib.sqlmodel import Lead


class TestSQLModelLead:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            Lead as SALead,
        )

        assert Lead is SALead
