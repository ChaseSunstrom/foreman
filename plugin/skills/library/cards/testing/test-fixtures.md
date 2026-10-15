---
name: test-fixtures
title: Test fixtures
area: testing
tags: [testing, fixtures, setup, teardown, pytest, jest, data]
detect: []
related: [test-data-factories, test-isolation, database-tests, unit-test-design]
---
Fixtures build the preconditions of a test: small, scoped, explicit, with guaranteed cleanup and visible values.

## Verify
- `pytest --setup-show -q path/to/test.py`: shows which fixtures run, in what order and scope (pytest).
- `pytest --fixtures -q`: lists available fixtures with their docstrings.
- `npx jest --verbose path/to/file.test.js`: setup hooks and test order for the file (Jest).
- `go test -v -run TestName ./pkg`: `t.Cleanup` runs and subtests report individually (Go).

## Test first
Fixtures should create the state and clean it up, and the test should state which values matter.
```python
import pytest

@pytest.fixture
def user(db):
    u = db.create_user(email="a@b.co", role="member")
    yield u
    db.delete_user(u.id)

def test_member_cannot_delete_project(user, project_owned_by_other):
    assert not can_delete(user, project_owned_by_other)
```
Write the test first with the fixture name you wish existed; the missing fixture is the red state.

## Do
- Default to function scope. Widen to module or session only for read-only, expensive resources (compiled schema, container).
- Use `yield` fixtures or `t.Cleanup` / `afterEach` so teardown runs even when the test fails.
- Make the relevant values visible in the test (`role="member"`), and leave irrelevant ones to defaults.
- Compose small fixtures instead of one large "world" fixture.
- Put shared fixtures in `conftest.py` (pytest) or a `testutil` package; keep one-off fixtures next to their test.
- Return fresh mutable objects each time; return immutable ones freely.
- Prefer builders or factories over static JSON for data that varies per test.
- Name fixtures for what they provide (`logged_in_admin`), not how they are made.

## Avoid
- `autouse` fixtures that quietly seed data: hidden coupling and slow tests. Request fixtures explicitly.
- Session-scoped mutable fixtures: one test's change leaks to the rest. Keep them function-scoped or copy on use.
- Huge shared fixture files loaded for every test: slow and opaque. Build the minimum per test.
- Setup that depends on test order (`test_1` creates, `test_2` uses): fails alone. Move creation into a fixture.
- Teardown written as the last test line: skipped on failure. Use `yield` or a cleanup hook.
- Fixtures that assert: failures show up as errors in setup, not the test. Keep assertions in tests.

## Review
- [ ] Fixtures are function-scoped unless immutable and costly.
- [ ] Cleanup runs on failure.
- [ ] Each test shows the values its outcome depends on.
- [ ] No autouse data seeding or order dependence.
- [ ] Fixtures are small, composable and named for what they provide.
