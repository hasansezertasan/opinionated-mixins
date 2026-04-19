from opinionated_mixins.contrib.sqlmodel import IntegerID


class TestSQLModelIntegerID:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            IntegerID as SAIntegerID,
        )

        assert IntegerID is SAIntegerID
