from opinionated_mixins.contrib.sqlmodel import User


class TestSQLModelUser:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            User as SAUser,
        )

        assert User is SAUser
