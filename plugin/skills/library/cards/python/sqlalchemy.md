---
name: sqlalchemy
title: SQLAlchemy
area: python
tags: [python, orm, sql, sqlalchemy, sessions, async]
detect: [dep:sqlalchemy, dep:SQLAlchemy, dep:sqlmodel]
related: [alembic, pydantic, fastapi, pytest, flask]
---
SQLAlchemy 2.x: typed declarative models, `select()` queries, `Session` and `AsyncSession` lifecycle.

## Verify
- `python -c "import sqlalchemy; print(sqlalchemy.__version__)"`: the major version matches the style in the code (1.x vs 2.x).
- `python -W error::sqlalchemy.exc.SADeprecationWarning -m pytest -q`: 1.x-style legacy calls fail.
- `alembic check`: models and migrations agree (when Alembic is used).
- `pytest -q`: the suite against a test database.

## Test first
Run against a real engine (SQLite in memory or a throwaway Postgres) and roll back per test.
```python
import pytest
from sqlalchemy import select
from app.models import User

def test_email_unique(session):
    session.add(User(email="a@x.io"))
    session.flush()
    session.add(User(email="a@x.io"))
    with pytest.raises(Exception):
        session.flush()
```
Fixture: bind a connection, begin a transaction, yield a `Session(bind=conn)`, roll back.

## Do
- Declare models with `DeclarativeBase`, `Mapped[...]` and `mapped_column(...)`.
- Query with `session.execute(select(User).where(...)).scalars()`; use `session.get(User, pk)` for key lookups.
- Scope one session per unit of work (request, task) with `with Session(engine) as s, s.begin():` so commit or rollback is automatic.
- Set `relationship(lazy="raise")` or use `selectinload`/`joinedload` options explicitly to prevent hidden N+1.
- Put `UniqueConstraint`, `Index` and `CheckConstraint` in `__table_args__`.
- For async use `create_async_engine`, `async_sessionmaker(expire_on_commit=False)` and `await session.execute(...)`.
- Create the engine once per process; set `pool_pre_ping=True` for long-lived pools.

## Avoid
- `session.query(...)` and `declarative_base()` from 1.x tutorials: legacy. Use `select()` and `DeclarativeBase`.
- Lazy-loading a relationship in `AsyncSession`: raises `MissingGreenlet`. Eager load or `await session.run_sync(...)`.
- `expire_on_commit=True` with async sessions then reading attributes after commit: the same error. Disable it.
- Sharing a `Session` across threads or concurrent tasks: not safe. One per task.
- Building SQL with f-strings in `text()`: injection. Use bound parameters (`text("... :id")`, `{"id": x}`).
- `Base.metadata.create_all()` as the production schema path: use migrations.
- Catching `IntegrityError` and continuing on the same session: it needs `rollback()` first.

## Review
- [ ] All queries use 2.x `select()`; no `session.query`.
- [ ] Session lifetime is explicit and one-per-request or task, with commit and rollback in one place.
- [ ] Relationship loading strategy is stated for every list query.
- [ ] Constraints are in the schema, not only validated in Python.
- [ ] Raw SQL uses bound parameters.
