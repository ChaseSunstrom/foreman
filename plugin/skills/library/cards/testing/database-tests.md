---
name: database-tests
title: Database tests
area: testing
tags: [testing, database, sql, transactions, testcontainers, integration, isolation]
detect: []
related: [integration-testing, test-isolation, migration-tests, test-data-factories, test-fixtures]
---
Test data access against the real engine you ship, isolate each test in a rollback or fresh schema, and prove constraints and queries.

## Verify
- `docker run --rm -d -e POSTGRES_PASSWORD=t -p 5433:5432 postgres:16`: a disposable real database for local runs (use your engine and tag).
- `pytest -q tests/db` (or `go test ./internal/store/...`, `npx jest tests/db`): the data-layer suite passes.
- `psql "$TEST_DATABASE_URL" -c '\dt'`: the schema exists exactly as migrations produce it (Postgres).
- `pytest -q -p randomly tests/db`: tests pass in random order, so none depend on leftover rows.

## Test first
Write the constraint or query test against a real database, inside a rolled-back transaction.
```python
def test_duplicate_email_is_rejected(db_session):
    db_session.add(User(email="a@b.co"))
    db_session.flush()
    db_session.add(User(email="a@b.co"))
    with pytest.raises(IntegrityError):
        db_session.flush()
```
The fixture opens a transaction (or a savepoint) per test and rolls back in teardown.

## Do
- Use the same engine and major version as production (a Testcontainers or Docker database), not SQLite as a stand-in.
- Build the schema from the real migrations once per session; isolate each test by transaction rollback, truncation or a schema per worker.
- Assert the constraints you rely on: unique, foreign key, not null, check. Test the failure, not only success.
- Test the queries that matter with realistic row counts and the edge cases: empty, one, many, NULLs, duplicates, ordering ties.
- Check that transactions commit and roll back as designed: force an error mid-way and assert nothing persisted.
- Give each parallel worker its own database or schema name.
- Use factories for rows; insert only the columns the test depends on.
- Assert on query count for hot paths to catch N+1 regressions.

## Avoid
- An in-memory fake engine with different SQL semantics: dialect and constraint bugs pass. Use the real engine.
- Tests that share rows and assume counts: order-dependent. Isolate per test and assert on own ids.
- Mocking the repository when testing the repository: the SQL is never run. Mock above it, not in it.
- Committing inside a test that expects rollback isolation: data leaks. Use savepoints or truncate after.
- Schema created from ORM models while production uses migrations: drift. Apply the migrations.
- Time-dependent or ordering-dependent queries without explicit `ORDER BY`: flaky. Order explicitly.

## Review
- [ ] Real engine and version, schema from migrations.
- [ ] Each test is isolated and parallel-safe.
- [ ] Constraint violations and rollback paths are tested.
- [ ] Queries have edge-case data and explicit ordering.
- [ ] No mocks inside the layer under test.
