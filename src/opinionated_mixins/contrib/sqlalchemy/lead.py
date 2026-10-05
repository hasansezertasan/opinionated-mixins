from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus

from sqlalchemy import Boolean, Column, Date, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Lead:
    """Lead mixin for SQLAlchemy models."""

    __abstract__ = True

    title = Column(String(255), nullable=True)
    salutation = Column(String(64), nullable=True)
    job_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    status = Column(Enum(LeadStatus), nullable=True)
    source = Column(Enum(LeadSource), nullable=True)
    industry = Column(String(255), nullable=True)
    rating = Column(Enum(LeadRating), nullable=True)
    opportunity_amount = Column(Numeric(precision=12, scale=2), nullable=True)
    currency = Column(String(3), nullable=True)
    probability = Column(Integer, nullable=True, default=0)
    close_date = Column(Date, nullable=True)
    last_contacted = Column(Date, nullable=True)
    next_follow_up = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
