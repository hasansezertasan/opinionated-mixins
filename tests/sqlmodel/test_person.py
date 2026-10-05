from opinionated_mixins.contrib.sqlmodel import Person


class TestSQLModelPerson:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            Person as SAPerson,
        )

        assert Person is SAPerson
