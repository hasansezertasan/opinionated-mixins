from opinionated_mixins.contrib.sqlmodel import Announcement


class TestSQLModelAnnouncement:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            Announcement as SAAnnouncment,
        )

        assert Announcement is SAAnnouncment
