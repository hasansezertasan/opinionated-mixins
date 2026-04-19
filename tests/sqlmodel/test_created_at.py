from opinionated_mixins.contrib.sqlmodel import CreatedAt


class TestSQLModelCreatedAt:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            CreatedAt as SACreatedAt,
        )

        assert CreatedAt is SACreatedAt
