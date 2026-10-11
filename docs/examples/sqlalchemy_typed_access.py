"""Read SQLAlchemy mixin fields as plain Python values.

The SQLAlchemy mixins expose ``Mapped[...]`` annotations to type checkers, so
instance attributes are typed as their Python values rather than ``Column``
objects. The type checkers in the ``style`` environment verify this module.
"""

import datetime
import uuid
from decimal import Decimal

from opinionated_mixins.contrib.sqlalchemy import (
    UUIDID,
    Activity,
    Announcement,
    IntegerID,
    Lead,
    User,
)
from opinionated_mixins.enums import AnnouncementCategory, LeadStatus
from sqlalchemy import Select, orm, select


class Base(orm.DeclarativeBase):
    """Declarative base for the example models."""


class Account(IntegerID, User, Base):
    """User account keyed by an auto-incrementing integer."""

    __tablename__ = "accounts"


class SalesLead(UUIDID, Lead, Base):
    """Sales lead keyed by a UUID."""

    __tablename__ = "sales_leads"


class News(IntegerID, Announcement, Base):
    """Site-wide announcement."""

    __tablename__ = "news"


class Event(IntegerID, Activity, Base):
    """Activity stream entry."""

    __tablename__ = "events"


def account_summary(account: Account) -> tuple[int, str, str | None]:
    """Return an account's id, username, and optional email.

    Returns:
        tuple[int, str, str | None]: The account's typed field values.
    """
    return account.id, account.username, account.email


def lead_pipeline(
    lead: SalesLead,
) -> tuple[uuid.UUID, LeadStatus | None, Decimal | None, datetime.date | None, bool]:
    """Return a lead's id and pipeline fields.

    Returns:
        tuple[uuid.UUID, LeadStatus | None, Decimal | None, datetime.date | None,
        bool]: The lead's typed field values.
    """
    return (
        lead.id,
        lead.status,
        lead.opportunity_amount,
        lead.close_date,
        lead.is_active,
    )


def news_category(news: News) -> AnnouncementCategory:
    """Return an announcement's category.

    Returns:
        AnnouncementCategory: The announcement's category.
    """
    return news.category


def event_details(event: Event) -> tuple[datetime.datetime, dict[str, object] | None]:
    """Return when an activity happened and its JSON payload.

    Returns:
        tuple[datetime.datetime, dict[str, object] | None]: The typed values.
    """
    return event.created_at, event.data


def accounts_named(username: str) -> Select[tuple[Account]]:
    """Build a query that filters on a mixin column at class level.

    Returns:
        Select[tuple[Account]]: A select statement for matching accounts.
    """
    return select(Account).where(Account.username == username)
