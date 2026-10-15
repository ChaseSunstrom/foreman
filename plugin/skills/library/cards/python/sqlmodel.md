---
name: sqlmodel
title: SQLModel
area: python
tags: [python, orm, pydantic, sqlalchemy, fastapi, sql]
detect: [dep:sqlmodel]
related: [sqlalchemy, pydantic, fastapi, alembic, pytest]
---
SQLModel: Pydantic plus SQLAlchemy models, with separate table and API schemas and one session per request.

## Verify
- `pytest -q`: tests against an in-memory or temp SQLite engine.
- `alembic upgrade head && alembic check`: migrations apply and match the models (`alembic check` needs a recent Alembic).
- `pyright` (or `mypy .`): typed fields and queries.
- `python -c "from sqlmodel import SQLModel; import app.models; print(SQLModel.metadata.tables.keys())"`: every table is registered by import.

## Test first
```python
import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from app.models import Hero

@pytest.fixture
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s

def test_unique_name(session):
    session.add(Hero(name="a")); session.commit()
    assert session.exec(select(Hero).where(Hero.name == "a")).one().id is not None
```

## Do
- Table models use `class Hero(SQLModel, table=True)` with `id: int | None = Field(default=None, primary_key=True)`.
- Separate schemas without `table=True`: `HeroCreate`, `HeroPublic`, `HeroUpdate`. Never use the table class as request input.
- Query with `session.exec(select(Hero).where(...))` and `.first()`, `.one()` or `.all()`.
- Partial updates: `data = body.model_dump(exclude_unset=True)` then `hero.sqlmodel_update(data)`.
- Declare relations with `Relationship(back_populates=...)`. Use `selectinload` through `.options(...)` to avoid N+1.
- Add `index=True` and `unique=True` through `Field`. Use `sa_column` for anything `Field` cannot express.
- Manage schema with Alembic. Import all models in `env.py` and set `target_metadata = SQLModel.metadata`.

## Avoid
- `SQLModel.metadata.create_all` in production instead of migrations: no schema evolution. Use Alembic.
- Using `session.query(...)`: the legacy style. Use `session.exec(select(...))`.
- Validation expected on table models: `table=True` models skip Pydantic validation on init. Validate via a non-table schema with `model_validate`.
- Sharing one `Session` globally: not thread safe. One per request via a dependency.
- Reading relationships after the session closes: `DetachedInstanceError`. Eager load or return a public schema.
- Forgetting to import a model module before `create_all` or autogenerate: the table is missing.

## Review
- [ ] Request and response types are non-table schemas.
- [ ] Sessions are scoped per request and committed or rolled back in one place.
- [ ] Relationships are eager loaded where lists are returned.
- [ ] Alembic revision exists for every model change.
- [ ] Update endpoints use `exclude_unset=True`.
