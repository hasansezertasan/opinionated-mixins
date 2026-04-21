"""Flask-Admin example showcasing all opinionated-mixins with SQLAlchemy.

Run:
    pip install flask flask-admin sqlalchemy opinionated-mixins
    python app.py

Then visit http://localhost:5000/admin/
"""

from __future__ import annotations

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from opinionated_mixins.contrib.sqlalchemy import (
    UUIDID,
    Announcement,
    CreatedAt,
    Feedback,
    IntegerID,
    IsActive,
    Lead,
    Person,
    Template,
    UpdatedAt,
    User,
)
from opinionated_mixins.enums import (
    AnnouncementCategory,
    FeedbackCategory,
    FeedbackStatus,
    LeadRating,
    LeadSource,
    LeadStatus,
    TemplateFormat,
    TemplateType,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    """Shared declarative base for all models."""


class AnnouncementModel(IntegerID, CreatedAt, IsActive, Announcement, Base):
    """Announcement with auto-increment ID, timestamp, and soft-delete."""

    __tablename__ = "announcements"


class FeedbackModel(IntegerID, CreatedAt, UpdatedAt, Feedback, Base):
    """Feedback with auto-increment ID and both timestamps."""

    __tablename__ = "feedbacks"


class TemplateModel(IntegerID, CreatedAt, UpdatedAt, Template, Base):
    """Template with auto-increment ID and both timestamps."""

    __tablename__ = "templates"


class LeadModel(IntegerID, CreatedAt, UpdatedAt, Lead, Base):
    """Lead with auto-increment ID and both timestamps.

    Note: Lead mixin already includes its own ``is_active`` field,
    so the separate ``IsActive`` mixin is not needed here.
    """

    __tablename__ = "leads"


class PersonModel(IntegerID, Person, Base):
    """Person with auto-increment ID."""

    __tablename__ = "persons"


class UserModel(UUIDID, CreatedAt, User, Base):
    """User with UUID primary key and creation timestamp."""

    __tablename__ = "users"


# ---------------------------------------------------------------------------
# Flask-Admin views
# ---------------------------------------------------------------------------


class AnnouncementAdmin(ModelView):
    """Admin view for announcements."""

    column_list = [
        "id",
        "title",
        "category",
        "is_active",
        "created_at",
    ]
    column_searchable_list = ["title", "content"]
    column_filters = ["category", "is_active", "created_at"]
    form_choices = {
        "category": [(c.value, c.name) for c in AnnouncementCategory],
    }


class FeedbackAdmin(ModelView):
    """Admin view for feedback submissions."""

    column_list = [
        "id",
        "subject",
        "category",
        "status",
        "created_at",
        "updated_at",
    ]
    column_searchable_list = ["subject", "content"]
    column_filters = ["category", "status"]
    form_choices = {
        "category": [(c.value, c.name) for c in FeedbackCategory],
        "status": [(s.value, s.name) for s in FeedbackStatus],
    }


class TemplateAdmin(ModelView):
    """Admin view for templates."""

    column_list = [
        "id",
        "name",
        "format",
        "type",
        "created_at",
        "updated_at",
    ]
    column_searchable_list = ["name", "content"]
    column_filters = ["format", "type"]
    form_choices = {
        "format": [(f.value, f.name) for f in TemplateFormat],
        "type": [(t.value, t.name) for t in TemplateType],
    }


class LeadAdmin(ModelView):
    """Admin view for leads."""

    column_list = [
        "id",
        "title",
        "company_name",
        "status",
        "source",
        "rating",
        "opportunity_amount",
        "is_active",
        "created_at",
    ]
    column_searchable_list = ["title", "company_name"]
    column_filters = ["status", "source", "rating", "is_active"]
    form_choices = {
        "status": [(s.value, s.name) for s in LeadStatus],
        "source": [(s.value, s.name) for s in LeadSource],
        "rating": [(r.value, r.name) for r in LeadRating],
    }


class PersonAdmin(ModelView):
    """Admin view for persons."""

    column_list = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "city",
        "country",
    ]
    column_searchable_list = ["first_name", "last_name", "email"]
    column_filters = ["country", "city"]


class UserAdmin(ModelView):
    """Admin view for users."""

    column_list = [
        "id",
        "username",
        "email",
        "date_email_verified",
        "created_at",
    ]
    column_searchable_list = ["username", "email"]
    column_filters = ["date_email_verified", "created_at"]
    form_excluded_columns = ["hashed_password"]


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------


def seed(session: Session) -> None:
    """Insert sample records so the admin UI isn't empty on first launch."""
    if session.query(AnnouncementModel).count():
        return

    session.add_all(
        [
            AnnouncementModel(
                title="Scheduled maintenance",
                content="Systems will be down Saturday 02:00-04:00 UTC.",
                category=AnnouncementCategory.MAINTENANCE,
            ),
            AnnouncementModel(
                title="New feature: Dark mode",
                content="Dark mode is now available in settings.",
                category=AnnouncementCategory.UPDATE,
            ),
            FeedbackModel(
                subject="Login page slow",
                content="Takes 5+ seconds to load on mobile.",
                category=FeedbackCategory.BUG,
                status=FeedbackStatus.PENDING,
            ),
            TemplateModel(
                name="Welcome email",
                content="Hi {{ name }}, welcome aboard!",
                format=TemplateFormat.HTML,
                type=TemplateType.EMAIL,
            ),
            LeadModel(
                title="Mr.",
                company_name="Acme Corp",
                status=LeadStatus.IN_PROCESS,
                source=LeadSource.CALL,
                rating=LeadRating.HOT,
            ),
            PersonModel(
                first_name="Ada",
                last_name="Lovelace",
                email="ada@example.com",
                city="London",
                country="GB",
            ),
            UserModel(
                username="admin",
                hashed_password="pbkdf2:sha256:placeholder",
                email="admin@example.com",
            ),
        ],
    )
    session.commit()


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-only-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"

    engine = create_engine("sqlite:///demo.db")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    with session_factory() as seed_session:
        seed(seed_session)

    admin = Admin(app, name="Opinionated Mixins", template_mode="bootstrap4")
    admin.add_view(AnnouncementAdmin(AnnouncementModel, session, name="Announcements"))
    admin.add_view(FeedbackAdmin(FeedbackModel, session, name="Feedback"))
    admin.add_view(TemplateAdmin(TemplateModel, session, name="Templates"))
    admin.add_view(LeadAdmin(LeadModel, session, name="Leads"))
    admin.add_view(PersonAdmin(PersonModel, session, name="Persons"))
    admin.add_view(UserAdmin(UserModel, session, name="Users"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
