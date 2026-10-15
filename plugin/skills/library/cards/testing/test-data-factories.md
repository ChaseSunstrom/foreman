---
name: test-data-factories
title: Test data factories
area: testing
tags: [factories, fixtures, builders, faker, test-data, seeds]
detect: [dep:factory-boy, dep:faker, dep:@faker-js/faker, dep:fishery, dep:factory_bot, dep:polyfactory, dep:bogus]
related: [unit-test-design, integration-testing, api-testing, flaky-tests]
---
Factories build valid objects with sensible defaults so each test states only the fields that matter to it.

## Verify
- `pytest -q -p no:randomly tests && pytest -q -p randomly tests` (pytest-randomly): factories produce independent data under shuffled order.
- `pytest -q -x tests/test_factories.py`: each factory's default object passes validation and saves.
- `bundle exec rspec spec/factories_spec.rb`: FactoryBot lint spec (one that calls `FactoryBot.lint`) passes.
- `npx jest --runInBand` then `npx jest`: same result serial and parallel, so ids and uniques do not collide.

## Test first
The test overrides only the field it is about; a factory for a valid default exists first.
```python
def test_expired_subscription_blocks_download():
    user = UserFactory(subscription=SubscriptionFactory(expires_at=days_ago(1)))
    resp = client_for(user).get("/download/1")
    assert resp.status_code == 402
```
Factories live in `tests/factories.py`, `spec/factories/` or `test/support/factories.ts`.

## Do
- Default every field to a valid, minimal object; override per test only the field under test.
- Seed fake data (`Faker.seed(n)`, `faker.seed(n)`) and print the seed, so a failure reproduces.
- Use sequences for unique fields (emails, slugs) instead of random values that can collide.
- Create associations lazily (`SubFactory`, `association`), and offer a build-only strategy that skips the database.
- Provide named traits or variants (`admin`, `expired`) for common states.
- Keep factories next to the schema and lint them in a test so schema changes break loudly.
- Return domain objects in unit tests and persist only in integration tests.

## Avoid
- Large shared fixture files (YAML, SQL dumps) used by every test: hidden coupling, unclear intent. Use factories with overrides.
- Random data with no seed: unreproducible failures. Seed and log it.
- Faker for unique constraints without sequences: rare collision flakes. Use sequences.
- Factories that persist by default in unit tests: slow. Use build or in-memory.
- Hard-coded ids and relationships in factories: collisions across tests. Let the database assign them.
- Defaults that encode a business scenario (a premium user): surprises in other tests. Make the default the plain case.

## Review
- [ ] Each test overrides only fields relevant to its behavior.
- [ ] Unique fields use sequences.
- [ ] Random data is seeded and the seed is reported.
- [ ] A lint test validates every factory.
- [ ] Unit tests build without touching the database.
