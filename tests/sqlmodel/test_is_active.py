from opinionated_mixins.contrib.sqlmodel import IsActive


class TestSQLModelIsActive:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            IsActive as SAIsActive,
        )

        assert IsActive is SAIsActive
