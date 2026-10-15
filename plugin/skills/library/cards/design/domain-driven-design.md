---
name: domain-driven-design
title: Domain-driven design
area: design
tags: [ddd, aggregates, value-objects, bounded-context, domain-model, invariants]
detect: []
related: [hexagonal-architecture, event-sourcing, modular-monolith, state-machines, sagas]
---
Model the business with a shared language, bounded contexts and aggregates that guard their own invariants.

## Verify
- `pytest -q tests/domain`: domain rules run without a database, framework or network.
- `grep -rnE "^(import|from) .*(sqlalchemy|django|flask|fastapi|requests)" src/domain`: no infrastructure imports in the domain (expect no output).
- `grep -rnE "\.(status|state)\s*=" src --include=*.py | grep -v "src/domain"`: state fields are mutated only by domain methods (expect no output; adjust to your fields).

## Test first
Express an invariant as a failing test against the aggregate.
```python
def test_order_total_cannot_exceed_credit_limit():
    order = Order.new(customer_credit_limit=Money(100, "USD"))
    order.add_line(sku="A", price=Money(60, "USD"), qty=1)
    with pytest.raises(CreditLimitExceeded):
        order.add_line(sku="B", price=Money(50, "USD"), qty=1)
    assert order.total == Money(60, "USD")        # failed command changed nothing
```

## Do
- Use the business's words for class and method names (`order.ship()`, not `order.setStatus(3)`), and keep a glossary per context.
- Draw bounded contexts around language and ownership. The same word can mean different models in each (Customer in sales versus support).
- Make aggregates small, with one root. Enforce invariants inside it, and reference other aggregates by ID.
- Modify one aggregate per transaction. Coordinate across aggregates with domain events and eventual consistency.
- Use value objects (immutable, compared by value) for money, quantities, emails and ranges, and validate in the constructor.
- Make illegal states unrepresentable: enums or sum types for states, and no public setters.
- Keep domain services for logic that spans aggregates. Keep repositories to one per aggregate root, returning whole aggregates.
- Translate at context borders with an anti-corruption layer rather than adopting another model's types.

## Avoid
- Anemic models (data classes plus `OrderService` holding all the rules): invariants scatter and break. Put behavior on the entity.
- Large aggregates loading half the database to enforce a loose rule: contention and slow loads. Split, and enforce the rule eventually.
- Aggregates holding object references to others: loading and locking spread. Use IDs.
- Primitive obsession (`float` for money, `str` for email): rounding and invalid values leak in. Use value objects, and `Decimal` or integer minor units.
- One universal model shared by all contexts: it becomes a lowest common denominator. Separate models and map at the edge.
- Applying DDD tactics to a simple CRUD area: it adds ceremony with no payoff. Keep plain tables there.
- Repositories exposing query-builder or ORM types to the domain.

## Review
- [ ] Names match the ubiquitous language, with a glossary kept.
- [ ] Each invariant has one owner (an aggregate) and a test.
- [ ] Transactions touch one aggregate, and cross-aggregate links are IDs.
- [ ] Value objects replace primitives for money, time ranges and identifiers.
- [ ] The domain package has no infrastructure imports.
