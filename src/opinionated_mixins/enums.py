# SPDX-FileCopyrightText: 2024-present hasansezertasan <hasansezertasan@gmail.com>
#
# SPDX-License-Identifier: MIT
import enum


class AnnouncementCategory(str, enum.Enum):
    """Category of an announcement."""

    GENERAL = "general"
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    UPDATE = "update"
    EVENT = "event"
