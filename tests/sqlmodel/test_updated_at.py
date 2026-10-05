from opinionated_mixins.contrib.sqlmodel import UpdatedAt


class TestSQLModelUpdatedAt:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            UpdatedAt as SAUpdatedAt,
        )

        assert UpdatedAt is SAUpdatedAt
