Usage
=====

Opinionated Mixins exposes framework-specific mixins from
``opinionated_mixins.contrib``. For example, SQLAlchemy users can import a mixin
directly from its integration package:

.. code-block:: python

   from opinionated_mixins.contrib.sqlalchemy import CreatedAt

See the :doc:`modules` reference for the supported framework integrations and
the `README <https://github.com/hasansezertasan/opinionated-mixins#readme>`_
for usage examples.

Indexing Recommendations
------------------------

SQLAlchemy mixins intentionally do not set ``index=True`` on any column.
The library cannot anticipate an application's specific query patterns, and baked-in
indexes add unnecessary write overhead and are difficult to opt out of.

Consumers should declare indexes explicitly on their concrete models using
``__table_args__`` according to their query and access patterns:

.. code-block:: python

   from opinionated_mixins.contrib.sqlalchemy import Announcement
   from sqlalchemy import Column, Index, Integer
   from sqlalchemy.orm import DeclarativeBase


   class Base(DeclarativeBase):
       pass


   class MyAnnouncement(Announcement, Base):
       __tablename__ = "announcements"

       id = Column(Integer, primary_key=True)

       __table_args__ = (
           Index("ix_announcements_title", "title"),
       )

Each mixin docstring includes specific indexing recommendations and examples for its fields.

