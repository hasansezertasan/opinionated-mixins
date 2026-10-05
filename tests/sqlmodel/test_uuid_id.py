from opinionated_mixins.contrib.sqlmodel import UUIDID


class TestSQLModelUUIDID:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            UUIDID as SAUUIDID,
        )

        assert UUIDID is SAUUIDID
