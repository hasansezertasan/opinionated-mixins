"""Flask-Admin example showcasing all opinionated-mixins with MongoEngine.

Run with real MongoDB:
    pip install flask flask-admin mongoengine opinionated-mixins
    python app.py

Run without MongoDB (mongomock):
    pip install flask flask-admin mongoengine mongomock opinionated-mixins
    MONGOMOCK=1 python app.py

Then visit http://localhost:5000/admin/
"""

from __future__ import annotations

import os

import mongoengine
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from mongoengine import Document
from opinionated_mixins.contrib.mongoengine import (
    Announcement,
    CreatedAt,
    Feedback,
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

# ---------------------------------------------------------------------------
# Document models
# ---------------------------------------------------------------------------


class AnnouncementDoc(CreatedAt, IsActive, Announcement, Document):
    """Announcement with creation timestamp and soft-delete."""

    meta = {"collection": "announcements"}


class FeedbackDoc(CreatedAt, UpdatedAt, Feedback, Document):
    """Feedback with both timestamps."""

    meta = {"collection": "feedbacks"}


class TemplateDoc(CreatedAt, UpdatedAt, Template, Document):
    """Template with both timestamps."""

    meta = {"collection": "templates"}


class LeadDoc(CreatedAt, UpdatedAt, Lead, Document):
    """Lead with both timestamps.

    Note: Lead mixin already includes its own ``is_active`` field,
    so the separate ``IsActive`` mixin is not needed here.
    """

    meta = {"collection": "leads"}


class PersonDoc(Person, Document):
    """Person document."""

    meta = {"collection": "persons"}


class UserDoc(CreatedAt, User, Document):
    """User with creation timestamp."""

    meta = {"collection": "users"}


# ---------------------------------------------------------------------------
# Flask-Admin views
# ---------------------------------------------------------------------------


class AnnouncementAdmin(ModelView):
    """Admin view for announcements."""

    column_list = ["title", "category", "is_active", "created_at"]
    column_searchable_list = ["title", "content"]
    column_filters = ["category", "is_active", "created_at"]
    form_choices = {
        "category": [(c.value, c.name) for c in AnnouncementCategory],
    }


class FeedbackAdmin(ModelView):
    """Admin view for feedback submissions."""

    column_list = ["subject", "category", "status", "created_at", "updated_at"]
    column_searchable_list = ["subject", "content"]
    column_filters = ["category", "status"]
    form_choices = {
        "category": [(c.value, c.name) for c in FeedbackCategory],
        "status": [(s.value, s.name) for s in FeedbackStatus],
    }


class TemplateAdmin(ModelView):
    """Admin view for templates."""

    column_list = ["name", "format", "type", "created_at", "updated_at"]
    column_searchable_list = ["name", "content"]
    column_filters = ["format", "type"]
    form_choices = {
        "format": [(f.value, f.name) for f in TemplateFormat],
        "type": [(t.value, t.name) for t in TemplateType],
    }


class LeadAdmin(ModelView):
    """Admin view for leads."""

    column_list = [
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

    column_list = ["username", "email", "date_email_verified", "created_at"]
    column_searchable_list = ["username", "email"]
    column_filters = ["date_email_verified", "created_at"]
    form_excluded_columns = ["hashed_password"]


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------


def seed() -> None:
    """Insert sample records so the admin UI isn't empty on first launch."""
    if AnnouncementDoc.objects.count():
        return

    AnnouncementDoc(
        title="Scheduled maintenance",
        content="Systems will be down Saturday 02:00-04:00 UTC.",
        category=AnnouncementCategory.MAINTENANCE.value,
    ).save()
    AnnouncementDoc(
        title="New feature: Dark mode",
        content="Dark mode is now available in settings.",
        category=AnnouncementCategory.UPDATE.value,
    ).save()
    FeedbackDoc(
        subject="Login page slow",
        content="Takes 5+ seconds to load on mobile.",
        category=FeedbackCategory.BUG.value,
        status=FeedbackStatus.PENDING.value,
    ).save()
    TemplateDoc(
        name="Welcome email",
        content="Hi {{ name }}, welcome aboard!",
        format=TemplateFormat.HTML.value,
        type=TemplateType.EMAIL.value,
    ).save()
    LeadDoc(
        title="Mr.",
        company_name="Acme Corp",
        status=LeadStatus.IN_PROCESS.value,
        source=LeadSource.CALL.value,
        rating=LeadRating.HOT.value,
    ).save()
    PersonDoc(
        first_name="Ada",
        last_name="Lovelace",
        email="ada@example.com",
        city="London",
        country="GB",
    ).save()
    UserDoc(
        username="admin",
        hashed_password="pbkdf2:sha256:placeholder",
        email="admin@example.com",
    ).save()


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-only-secret-key"

    if os.environ.get("MONGOMOCK"):
        import mongomock

        mongoengine.connect(
            "opinionated_mixins_demo",
            mongo_client_class=mongomock.MongoClient,
        )
    else:
        mongoengine.connect(
            "opinionated_mixins_demo",
            host="mongodb://localhost:27017",
        )

    seed()

    admin = Admin(app, name="Opinionated Mixins (Mongo)", template_mode="bootstrap4")
    admin.add_view(AnnouncementAdmin(AnnouncementDoc, name="Announcements"))
    admin.add_view(FeedbackAdmin(FeedbackDoc, name="Feedback"))
    admin.add_view(TemplateAdmin(TemplateDoc, name="Templates"))
    admin.add_view(LeadAdmin(LeadDoc, name="Leads"))
    admin.add_view(PersonAdmin(PersonDoc, name="Persons"))
    admin.add_view(UserAdmin(UserDoc, name="Users"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
