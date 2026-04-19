import datetime
from decimal import Decimal

from opinionated_mixins.contrib.sqlalchemy import Lead
from opinionated_mixins.enums import LeadRating, LeadSource, LeadStatus
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyLead(Lead, Base):  # type: ignore[misc]
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)


LEAD_FIELDS = {
    "title",
    "salutation",
    "job_title",
    "company_name",
    "website",
    "linkedin_url",
    "status",
    "source",
    "industry",
    "rating",
    "opportunity_amount",
    "currency",
    "probability",
    "close_date",
    "last_contacted",
    "next_follow_up",
    "description",
    "is_active",
}


class TestSQLAlchemyLead:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_create_defaults(self) -> None:
        with Session(self.engine) as session:
            obj = MyLead()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.title is None
            assert obj.status is None
            assert obj.probability == 0
            assert obj.is_active is True

    def test_create_with_all_fields(self) -> None:
        with Session(self.engine) as session:
            obj = MyLead(
                title="Dr.",
                salutation="Dr.",
                job_title="CTO",
                company_name="Acme Inc.",
                website="https://acme.com",
                linkedin_url="https://linkedin.com/in/jane",
                status=LeadStatus.ASSIGNED,
                source=LeadSource.EMAIL,
                industry="Technology",
                rating=LeadRating.HOT,
                opportunity_amount=Decimal("50000.00"),
                currency="USD",
                probability=75,
                close_date=datetime.date(2026, 6, 1),
                last_contacted=datetime.date(2026, 4, 15),
                next_follow_up=datetime.date(2026, 4, 22),
                description="High-value lead",
                is_active=True,
            )
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.job_title == "CTO"
            assert obj.status == LeadStatus.ASSIGNED
            assert obj.source == LeadSource.EMAIL
            assert obj.rating == LeadRating.HOT
            assert obj.opportunity_amount == Decimal("50000.00")
            assert obj.probability == 75
            assert obj.close_date == datetime.date(2026, 6, 1)

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyLead.__table__.columns}
        assert LEAD_FIELDS.issubset(columns)
