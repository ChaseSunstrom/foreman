---
name: factory-boy
title: factory_boy
area: python
tags: [python, testing, fixtures, factories, django, sqlalchemy]
detect: [dep:factory-boy, dep:pytest-factoryboy]
related: [pytest, django-orm, sqlalchemy, faker, freezegun]
---
factory_boy: test data factories with sequences, sub-factories and traits, for Django, SQLAlchemy and plain classes.

## Verify
- `pytest -q`: tests that use the factories.
- `pytest -q -p no:randomly --create-db`: fresh test database when factory defaults changed (needs pytest-django).
- `python -c "import tests.factories"` (your module): factories import and declarations resolve.

## Test first
```python
import pytest
from tests.factories import OrderFactory

@pytest.mark.django_db
def test_paid_order_has_payment_and_total():
    order = OrderFactory(paid=True, items=3)
    assert order.payment is not None
    assert order.total == sum(i.price for i in order.items.all())
```
For SQLAlchemy, set `sqlalchemy_session` (or `sqlalchemy_session_factory`) in `class Meta` and `sqlalchemy_session_persistence = "flush"`.

## Do
- Use `factory.django.DjangoModelFactory` or `factory.alchemy.SQLAlchemyModelFactory` with `class Meta: model = Model`.
- Use `factory.Sequence(lambda n: f"user{n}@example.com")` for unique fields and `factory.Faker("email")` for realistic values.
- Link relations with `factory.SubFactory(UserFactory)`. Reverse relations use `factory.RelatedFactoryList`.
- Express variants with `class Params: paid = factory.Trait(status="paid")`.
- Compute from siblings with `factory.LazyAttribute(lambda o: o.first.lower())`.
- Use `@factory.post_generation` for many-to-many and extras. Check `create` and `extracted`.
- Use `Factory.build()` when no DB is needed and `create_batch(n)` for sets.
- Seed Faker with `factory.random.reseed_random(1234)` when failures must reproduce.
- Register with `pytest_factoryboy.register(UserFactory)` to get `user` and `user_factory` fixtures.

## Avoid
- Hard-coded unique values (`username="bob"`): collisions on the second create. Use `Sequence`.
- Factories that create the whole world by default: slow tests. Keep defaults minimal and add traits.
- Using `django_get_or_create` to hide unique collisions: results get order dependent. Use it only for lookup tables.
- Sharing the SQLAlchemy session globally across tests without rollback: state leaks. Bind it per test and roll back.
- Calling `Factory()` at import or module scope: runs without DB access. Create inside tests or fixtures.
- Using `factory.Faker` with `Sequence`-dependent assertions: random values break exact equality. Pass explicit values.

## Review
- [ ] Unique fields use sequences and relations use `SubFactory`.
- [ ] Defaults build the smallest valid object.
- [ ] Tests that assert on a field set it explicitly.
- [ ] Seeds are fixed where flakiness appeared.
