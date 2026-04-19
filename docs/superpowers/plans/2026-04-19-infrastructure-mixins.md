# Infrastructure Mixins Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add five granular infrastructure mixins (CreatedAt, UpdatedAt, IsActive, IntegerID, UUIDID) across all applicable frameworks.

**Architecture:** Each mixin gets its own file per framework, following existing patterns. SQLModel re-exports from SQLAlchemy. ID mixins are SQL-only (MongoEngine/ODMantic handle IDs natively). Cross-framework consistency test updated.

**Tech Stack:** SQLAlchemy (Column API), MongoEngine (field classes), ODMantic (Pydantic-style Field), pytest

---

### Task 1: CreatedAt — SQLAlchemy

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlalchemy/created_at.py`
- Test: `tests/sqlalchemy/test_created_at.py`

- [ ] **Step 1: Write the test file**

```python
import datetime

from opinionated_mixins.contrib.sqlalchemy import CreatedAt
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(CreatedAt, Base):  # type: ignore[misc]
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyCreatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_created_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.created_at is not None
            assert isinstance(obj.created_at, datetime.datetime)

    def test_created_at_not_null(self) -> None:
        col = MyModel.__table__.c.created_at
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "created_at" in columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlalchemy/test_created_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'CreatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/sqlalchemy/created_at.py`:

```python
import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class CreatedAt:
    """CreatedAt mixin for SQLAlchemy models."""

    __abstract__ = True

    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`:

```python
from .created_at import CreatedAt as CreatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlalchemy/test_created_at.py -v`
Expected: all 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlalchemy/created_at.py tests/sqlalchemy/test_created_at.py src/opinionated_mixins/contrib/sqlalchemy/__init__.py
git commit -m "feat: add CreatedAt mixin for SQLAlchemy"
```

---

### Task 2: CreatedAt — SQLModel re-export

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlmodel/created_at.py`
- Modify: `src/opinionated_mixins/contrib/sqlmodel/__init__.py`
- Test: `tests/sqlmodel/test_created_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlmodel import CreatedAt


class TestSQLModelCreatedAt:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            CreatedAt as SACreatedAt,
        )

        assert CreatedAt is SACreatedAt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlmodel/test_created_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'CreatedAt'`

- [ ] **Step 3: Create re-export file**

Create `src/opinionated_mixins/contrib/sqlmodel/created_at.py`:

```python
from opinionated_mixins.contrib.sqlalchemy.created_at import (
    CreatedAt as CreatedAt,
)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlmodel/__init__.py`:

```python
from .created_at import CreatedAt as CreatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlmodel/test_created_at.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlmodel/created_at.py tests/sqlmodel/test_created_at.py src/opinionated_mixins/contrib/sqlmodel/__init__.py
git commit -m "feat: add CreatedAt re-export for SQLModel"
```

---

### Task 3: CreatedAt — MongoEngine

**Files:**
- Create: `src/opinionated_mixins/contrib/mongoengine/created_at.py`
- Modify: `src/opinionated_mixins/contrib/mongoengine/__init__.py`
- Test: `tests/mongoengine/test_created_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.mongoengine import CreatedAt


class TestMongoEngineCreatedAt:
    def test_has_created_at_field(self) -> None:
        assert hasattr(CreatedAt, "created_at")

    def test_created_at_required(self) -> None:
        assert CreatedAt.created_at.required is True

    def test_created_at_has_default(self) -> None:
        assert CreatedAt.created_at.default is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/mongoengine/test_created_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'CreatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/mongoengine/created_at.py`:

```python
import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField


class CreatedAt:
    """CreatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    created_at = DateTimeField(
        required=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/mongoengine/__init__.py`:

```python
from .created_at import CreatedAt as CreatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/mongoengine/test_created_at.py -v`
Expected: all 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/mongoengine/created_at.py tests/mongoengine/test_created_at.py src/opinionated_mixins/contrib/mongoengine/__init__.py
git commit -m "feat: add CreatedAt mixin for MongoEngine"
```

---

### Task 4: CreatedAt — ODMantic

**Files:**
- Create: `src/opinionated_mixins/contrib/odmantic/created_at.py`
- Modify: `src/opinionated_mixins/contrib/odmantic/__init__.py`
- Test: `tests/odmantic/test_created_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.odmantic import CreatedAt


class TestODManticCreatedAt:
    def test_has_expected_annotations(self) -> None:
        annotations = CreatedAt.__annotations__
        assert "created_at" in annotations

    def test_created_at_has_default(self) -> None:
        field_info = CreatedAt.created_at.pydantic_field_info
        assert field_info.default_factory is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/odmantic/test_created_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'CreatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/odmantic/created_at.py`:

```python
import datetime

from odmantic import Field


class CreatedAt:
    """CreatedAt mixin for ODMantic models."""

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/odmantic/__init__.py`:

```python
from .created_at import CreatedAt as CreatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/odmantic/test_created_at.py -v`
Expected: all 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/odmantic/created_at.py tests/odmantic/test_created_at.py src/opinionated_mixins/contrib/odmantic/__init__.py
git commit -m "feat: add CreatedAt mixin for ODMantic"
```

---

### Task 5: UpdatedAt — SQLAlchemy

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlalchemy/updated_at.py`
- Modify: `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`
- Test: `tests/sqlalchemy/test_updated_at.py`

- [ ] **Step 1: Write the test file**

```python
import datetime

from opinionated_mixins.contrib.sqlalchemy import UpdatedAt
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(UpdatedAt, Base):  # type: ignore[misc]
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)


class TestSQLAlchemyUpdatedAt:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_updated_at_set_on_insert(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.updated_at is not None
            assert isinstance(obj.updated_at, datetime.datetime)

    def test_updated_at_changes_on_update(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel(name="original")
            session.add(obj)
            session.commit()
            session.refresh(obj)
            original_updated = obj.updated_at

            obj.name = "modified"
            session.commit()
            session.refresh(obj)
            assert obj.updated_at >= original_updated

    def test_updated_at_not_null(self) -> None:
        col = MyModel.__table__.c.updated_at
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "updated_at" in columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlalchemy/test_updated_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'UpdatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/sqlalchemy/updated_at.py`:

```python
import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UpdatedAt:
    """UpdatedAt mixin for SQLAlchemy models."""

    __abstract__ = True

    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`:

```python
from .updated_at import UpdatedAt as UpdatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlalchemy/test_updated_at.py -v`
Expected: all 4 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlalchemy/updated_at.py tests/sqlalchemy/test_updated_at.py src/opinionated_mixins/contrib/sqlalchemy/__init__.py
git commit -m "feat: add UpdatedAt mixin for SQLAlchemy"
```

---

### Task 6: UpdatedAt — SQLModel re-export

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlmodel/updated_at.py`
- Modify: `src/opinionated_mixins/contrib/sqlmodel/__init__.py`
- Test: `tests/sqlmodel/test_updated_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlmodel import UpdatedAt


class TestSQLModelUpdatedAt:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            UpdatedAt as SAUpdatedAt,
        )

        assert UpdatedAt is SAUpdatedAt
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlmodel/test_updated_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'UpdatedAt'`

- [ ] **Step 3: Create re-export file**

Create `src/opinionated_mixins/contrib/sqlmodel/updated_at.py`:

```python
from opinionated_mixins.contrib.sqlalchemy.updated_at import (
    UpdatedAt as UpdatedAt,
)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlmodel/__init__.py`:

```python
from .updated_at import UpdatedAt as UpdatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlmodel/test_updated_at.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlmodel/updated_at.py tests/sqlmodel/test_updated_at.py src/opinionated_mixins/contrib/sqlmodel/__init__.py
git commit -m "feat: add UpdatedAt re-export for SQLModel"
```

---

### Task 7: UpdatedAt — MongoEngine

**Files:**
- Create: `src/opinionated_mixins/contrib/mongoengine/updated_at.py`
- Modify: `src/opinionated_mixins/contrib/mongoengine/__init__.py`
- Test: `tests/mongoengine/test_updated_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.mongoengine import UpdatedAt


class TestMongoEngineUpdatedAt:
    def test_has_updated_at_field(self) -> None:
        assert hasattr(UpdatedAt, "updated_at")

    def test_updated_at_required(self) -> None:
        assert UpdatedAt.updated_at.required is True

    def test_updated_at_has_default(self) -> None:
        assert UpdatedAt.updated_at.default is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/mongoengine/test_updated_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'UpdatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/mongoengine/updated_at.py`:

```python
import datetime
from typing import Any, ClassVar

from mongoengine import DateTimeField


class UpdatedAt:
    """UpdatedAt mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    updated_at = DateTimeField(
        required=True,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/mongoengine/__init__.py`:

```python
from .updated_at import UpdatedAt as UpdatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/mongoengine/test_updated_at.py -v`
Expected: all 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/mongoengine/updated_at.py tests/mongoengine/test_updated_at.py src/opinionated_mixins/contrib/mongoengine/__init__.py
git commit -m "feat: add UpdatedAt mixin for MongoEngine"
```

---

### Task 8: UpdatedAt — ODMantic

**Files:**
- Create: `src/opinionated_mixins/contrib/odmantic/updated_at.py`
- Modify: `src/opinionated_mixins/contrib/odmantic/__init__.py`
- Test: `tests/odmantic/test_updated_at.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.odmantic import UpdatedAt


class TestODManticUpdatedAt:
    def test_has_expected_annotations(self) -> None:
        annotations = UpdatedAt.__annotations__
        assert "updated_at" in annotations

    def test_updated_at_has_default(self) -> None:
        field_info = UpdatedAt.updated_at.pydantic_field_info
        assert field_info.default_factory is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/odmantic/test_updated_at.py -v`
Expected: FAIL — `ImportError: cannot import name 'UpdatedAt'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/odmantic/updated_at.py`:

```python
import datetime

from odmantic import Field


class UpdatedAt:
    """UpdatedAt mixin for ODMantic models."""

    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/odmantic/__init__.py`:

```python
from .updated_at import UpdatedAt as UpdatedAt
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/odmantic/test_updated_at.py -v`
Expected: all 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/odmantic/updated_at.py tests/odmantic/test_updated_at.py src/opinionated_mixins/contrib/odmantic/__init__.py
git commit -m "feat: add UpdatedAt mixin for ODMantic"
```

---

### Task 9: IsActive — SQLAlchemy

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlalchemy/is_active.py`
- Modify: `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`
- Test: `tests/sqlalchemy/test_is_active.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlalchemy import IsActive
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(IsActive, Base):  # type: ignore[misc]
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)


class TestSQLAlchemyIsActive:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_is_active_defaults_true(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.is_active is True

    def test_is_active_can_be_set_false(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel(is_active=False)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.is_active is False

    def test_is_active_not_null(self) -> None:
        col = MyModel.__table__.c.is_active
        assert col.nullable is False

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "is_active" in columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlalchemy/test_is_active.py -v`
Expected: FAIL — `ImportError: cannot import name 'IsActive'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/sqlalchemy/is_active.py`:

```python
from sqlalchemy import Boolean, Column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IsActive:
    """IsActive mixin for SQLAlchemy models."""

    __abstract__ = True

    is_active = Column(Boolean, nullable=False, default=True)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`:

```python
from .is_active import IsActive as IsActive
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlalchemy/test_is_active.py -v`
Expected: all 4 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlalchemy/is_active.py tests/sqlalchemy/test_is_active.py src/opinionated_mixins/contrib/sqlalchemy/__init__.py
git commit -m "feat: add IsActive mixin for SQLAlchemy"
```

---

### Task 10: IsActive — SQLModel re-export

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlmodel/is_active.py`
- Modify: `src/opinionated_mixins/contrib/sqlmodel/__init__.py`
- Test: `tests/sqlmodel/test_is_active.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlmodel import IsActive


class TestSQLModelIsActive:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            IsActive as SAIsActive,
        )

        assert IsActive is SAIsActive
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlmodel/test_is_active.py -v`
Expected: FAIL — `ImportError: cannot import name 'IsActive'`

- [ ] **Step 3: Create re-export file**

Create `src/opinionated_mixins/contrib/sqlmodel/is_active.py`:

```python
from opinionated_mixins.contrib.sqlalchemy.is_active import (
    IsActive as IsActive,
)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlmodel/__init__.py`:

```python
from .is_active import IsActive as IsActive
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlmodel/test_is_active.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlmodel/is_active.py tests/sqlmodel/test_is_active.py src/opinionated_mixins/contrib/sqlmodel/__init__.py
git commit -m "feat: add IsActive re-export for SQLModel"
```

---

### Task 11: IsActive — MongoEngine

**Files:**
- Create: `src/opinionated_mixins/contrib/mongoengine/is_active.py`
- Modify: `src/opinionated_mixins/contrib/mongoengine/__init__.py`
- Test: `tests/mongoengine/test_is_active.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.mongoengine import IsActive


class TestMongoEngineIsActive:
    def test_has_is_active_field(self) -> None:
        assert hasattr(IsActive, "is_active")

    def test_is_active_required(self) -> None:
        assert IsActive.is_active.required is True

    def test_is_active_defaults_true(self) -> None:
        assert IsActive.is_active.default is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/mongoengine/test_is_active.py -v`
Expected: FAIL — `ImportError: cannot import name 'IsActive'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/mongoengine/is_active.py`:

```python
from typing import Any, ClassVar

from mongoengine import BooleanField


class IsActive:
    """IsActive mixin for MongoEngine documents."""

    meta: ClassVar[dict[str, Any]] = {"allow_inheritance": True}

    is_active = BooleanField(required=True, default=True)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/mongoengine/__init__.py`:

```python
from .is_active import IsActive as IsActive
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/mongoengine/test_is_active.py -v`
Expected: all 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/mongoengine/is_active.py tests/mongoengine/test_is_active.py src/opinionated_mixins/contrib/mongoengine/__init__.py
git commit -m "feat: add IsActive mixin for MongoEngine"
```

---

### Task 12: IsActive — ODMantic

**Files:**
- Create: `src/opinionated_mixins/contrib/odmantic/is_active.py`
- Modify: `src/opinionated_mixins/contrib/odmantic/__init__.py`
- Test: `tests/odmantic/test_is_active.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.odmantic import IsActive


class TestODManticIsActive:
    def test_has_expected_annotations(self) -> None:
        annotations = IsActive.__annotations__
        assert "is_active" in annotations

    def test_is_active_defaults_true(self) -> None:
        field_info = IsActive.is_active.pydantic_field_info
        assert field_info.default is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/odmantic/test_is_active.py -v`
Expected: FAIL — `ImportError: cannot import name 'IsActive'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/odmantic/is_active.py`:

```python
from odmantic import Field


class IsActive:
    """IsActive mixin for ODMantic models."""

    is_active: bool = Field(default=True)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/odmantic/__init__.py`:

```python
from .is_active import IsActive as IsActive
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/odmantic/test_is_active.py -v`
Expected: all 2 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/odmantic/is_active.py tests/odmantic/test_is_active.py src/opinionated_mixins/contrib/odmantic/__init__.py
git commit -m "feat: add IsActive mixin for ODMantic"
```

---

### Task 13: IntegerID — SQLAlchemy

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlalchemy/integer_id.py`
- Modify: `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`
- Test: `tests/sqlalchemy/test_integer_id.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlalchemy import IntegerID
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(IntegerID, Base):  # type: ignore[misc]
    __tablename__ = "items"


class TestSQLAlchemyIntegerID:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_id_is_primary_key(self) -> None:
        col = MyModel.__table__.c.id
        assert col.primary_key is True

    def test_id_auto_increments(self) -> None:
        with Session(self.engine) as session:
            obj1 = MyModel()
            obj2 = MyModel()
            session.add_all([obj1, obj2])
            session.commit()
            session.refresh(obj1)
            session.refresh(obj2)
            assert obj1.id == 1
            assert obj2.id == 2

    def test_id_is_integer(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert isinstance(obj.id, int)

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "id" in columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlalchemy/test_integer_id.py -v`
Expected: FAIL — `ImportError: cannot import name 'IntegerID'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/sqlalchemy/integer_id.py`:

```python
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IntegerID:
    """IntegerID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`:

```python
from .integer_id import IntegerID as IntegerID
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlalchemy/test_integer_id.py -v`
Expected: all 4 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlalchemy/integer_id.py tests/sqlalchemy/test_integer_id.py src/opinionated_mixins/contrib/sqlalchemy/__init__.py
git commit -m "feat: add IntegerID mixin for SQLAlchemy"
```

---

### Task 14: IntegerID — SQLModel re-export

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlmodel/integer_id.py`
- Modify: `src/opinionated_mixins/contrib/sqlmodel/__init__.py`
- Test: `tests/sqlmodel/test_integer_id.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlmodel import IntegerID


class TestSQLModelIntegerID:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            IntegerID as SAIntegerID,
        )

        assert IntegerID is SAIntegerID
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlmodel/test_integer_id.py -v`
Expected: FAIL — `ImportError: cannot import name 'IntegerID'`

- [ ] **Step 3: Create re-export file**

Create `src/opinionated_mixins/contrib/sqlmodel/integer_id.py`:

```python
from opinionated_mixins.contrib.sqlalchemy.integer_id import (
    IntegerID as IntegerID,
)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlmodel/__init__.py`:

```python
from .integer_id import IntegerID as IntegerID
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlmodel/test_integer_id.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlmodel/integer_id.py tests/sqlmodel/test_integer_id.py src/opinionated_mixins/contrib/sqlmodel/__init__.py
git commit -m "feat: add IntegerID re-export for SQLModel"
```

---

### Task 15: UUIDID — SQLAlchemy

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlalchemy/uuid_id.py`
- Modify: `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`
- Test: `tests/sqlalchemy/test_uuid_id.py`

- [ ] **Step 1: Write the test file**

```python
import uuid

from opinionated_mixins.contrib.sqlalchemy import UUIDID
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class MyModel(UUIDID, Base):  # type: ignore[misc]
    __tablename__ = "items"


class TestSQLAlchemyUUIDID:
    def setup_method(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def test_id_is_primary_key(self) -> None:
        col = MyModel.__table__.c.id
        assert col.primary_key is True

    def test_id_is_uuid(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert isinstance(obj.id, uuid.UUID)

    def test_id_auto_generated(self) -> None:
        with Session(self.engine) as session:
            obj = MyModel()
            session.add(obj)
            session.commit()
            session.refresh(obj)
            assert obj.id is not None

    def test_unique_ids(self) -> None:
        with Session(self.engine) as session:
            obj1 = MyModel()
            obj2 = MyModel()
            session.add_all([obj1, obj2])
            session.commit()
            session.refresh(obj1)
            session.refresh(obj2)
            assert obj1.id != obj2.id

    def test_fields_exist(self) -> None:
        columns = {c.name for c in MyModel.__table__.columns}
        assert "id" in columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlalchemy/test_uuid_id.py -v`
Expected: FAIL — `ImportError: cannot import name 'UUIDID'`

- [ ] **Step 3: Write the mixin**

Create `src/opinionated_mixins/contrib/sqlalchemy/uuid_id.py`:

```python
import uuid

from sqlalchemy import Column, Uuid
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class UUIDID:
    """UUIDID mixin for SQLAlchemy models."""

    __abstract__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlalchemy/__init__.py`:

```python
from .uuid_id import UUIDID as UUIDID
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlalchemy/test_uuid_id.py -v`
Expected: all 5 tests PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlalchemy/uuid_id.py tests/sqlalchemy/test_uuid_id.py src/opinionated_mixins/contrib/sqlalchemy/__init__.py
git commit -m "feat: add UUIDID mixin for SQLAlchemy"
```

---

### Task 16: UUIDID — SQLModel re-export

**Files:**
- Create: `src/opinionated_mixins/contrib/sqlmodel/uuid_id.py`
- Modify: `src/opinionated_mixins/contrib/sqlmodel/__init__.py`
- Test: `tests/sqlmodel/test_uuid_id.py`

- [ ] **Step 1: Write the test file**

```python
from opinionated_mixins.contrib.sqlmodel import UUIDID


class TestSQLModelUUIDID:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import (
            UUIDID as SAUUIDID,
        )

        assert UUIDID is SAUUIDID
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/sqlmodel/test_uuid_id.py -v`
Expected: FAIL — `ImportError: cannot import name 'UUIDID'`

- [ ] **Step 3: Create re-export file**

Create `src/opinionated_mixins/contrib/sqlmodel/uuid_id.py`:

```python
from opinionated_mixins.contrib.sqlalchemy.uuid_id import (
    UUIDID as UUIDID,
)
```

- [ ] **Step 4: Add export to `__init__.py`**

Add to `src/opinionated_mixins/contrib/sqlmodel/__init__.py`:

```python
from .uuid_id import UUIDID as UUIDID
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/sqlmodel/test_uuid_id.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/opinionated_mixins/contrib/sqlmodel/uuid_id.py tests/sqlmodel/test_uuid_id.py src/opinionated_mixins/contrib/sqlmodel/__init__.py
git commit -m "feat: add UUIDID re-export for SQLModel"
```

---

### Task 17: Update cross-framework consistency tests

**Files:**
- Modify: `tests/test_cross_framework_consistency.py`

- [ ] **Step 1: Update MIXIN_NAMES and add SQL-only handling**

The cross-framework consistency test needs to include new mixins. CreatedAt, UpdatedAt, and IsActive exist in all 4 frameworks. IntegerID and UUIDID exist only in SQLAlchemy and SQLModel.

Update `tests/test_cross_framework_consistency.py` — replace the `MIXIN_NAMES` list and add a new list plus test:

Replace:
```python
MIXIN_NAMES = ["Announcement", "Feedback", "Lead", "Person", "Template", "User"]
```

With:
```python
MIXIN_NAMES = [
    "Announcement",
    "CreatedAt",
    "Feedback",
    "IsActive",
    "Lead",
    "Person",
    "Template",
    "UpdatedAt",
    "User",
]

SQL_ONLY_MIXIN_NAMES = ["IntegerID", "UUIDID"]
```

- [ ] **Step 2: Add test for SQL-only mixins**

Add after existing tests:

```python
@pytest.mark.parametrize("mixin_name", SQL_ONLY_MIXIN_NAMES)
def test_sql_only_mixins_exported(mixin_name: str) -> None:
    """SQL-only mixins must be exported by sqlalchemy and sqlmodel."""
    for fw_name in ("sqlalchemy", "sqlmodel"):
        module = FRAMEWORKS[fw_name][0]
        assert hasattr(module, mixin_name), f"{fw_name} does not export {mixin_name}"


@pytest.mark.parametrize("mixin_name", SQL_ONLY_MIXIN_NAMES)
def test_sql_only_mixins_not_in_nosql(mixin_name: str) -> None:
    """SQL-only mixins must NOT be exported by mongoengine or odmantic."""
    for fw_name in ("mongoengine", "odmantic"):
        module = FRAMEWORKS[fw_name][0]
        assert not hasattr(module, mixin_name), (
            f"{fw_name} should not export {mixin_name}"
        )
```

- [ ] **Step 3: Run full test suite**

Run: `uv run pytest tests/test_cross_framework_consistency.py -v`
Expected: all tests PASS

- [ ] **Step 4: Run entire test suite to verify nothing broken**

Run: `uv run pytest tests -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_cross_framework_consistency.py
git commit -m "test: update cross-framework consistency for infrastructure mixins"
```

---

### Task 18: Lint, type-check, and final verification

**Files:** None (verification only)

- [ ] **Step 1: Run linter**

Run: `uv run ruff check .`
Expected: no errors

- [ ] **Step 2: Run formatter check**

Run: `uv run ruff format --check .`
Expected: no formatting issues (run `uv run ruff format .` to fix if needed)

- [ ] **Step 3: Run type checker**

Run: `uv run mypy --install-types --non-interactive src/opinionated_mixins`
Expected: no type errors

- [ ] **Step 4: Run full test suite with coverage**

Run: `uv run pytest tests -v`
Expected: all tests PASS

- [ ] **Step 5: Commit any lint/format fixes if needed**

```bash
git add -u
git commit -m "style: fix lint and formatting for infrastructure mixins"
```
