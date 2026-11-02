.. A 7-character "=" underline (the length of "Modules") is treated as a
   merge-conflict separator by ``git diff --check`` / ``check-merge-conflict``;
   keep this underline longer than the title to avoid the false positive.

Modules
=========

Opinionated Mixins provides framework-specific model mixins under
``opinionated_mixins.contrib``.

SQLAlchemy (``opinionated_mixins.contrib.sqlalchemy``)
------------------------------------------------------

Mixins for SQLAlchemy declarative models.

.. automodule:: opinionated_mixins.contrib.sqlalchemy

SQLModel (``opinionated_mixins.contrib.sqlmodel``)
--------------------------------------------------

Mixins for SQLModel models.

.. automodule:: opinionated_mixins.contrib.sqlmodel

MongoEngine (``opinionated_mixins.contrib.mongoengine``)
--------------------------------------------------------

Mixins for MongoEngine documents.

.. automodule:: opinionated_mixins.contrib.mongoengine

ODMantic (``opinionated_mixins.contrib.odmantic``)
--------------------------------------------------

Mixins for ODMantic models.

.. automodule:: opinionated_mixins.contrib.odmantic
