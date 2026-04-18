# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
from opinionated_mixins.contrib.sqlmodel import Announcement


class TestSQLModelAnnouncement:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            Announcement as SAAnnouncment,
        )

        assert Announcement is SAAnnouncment
