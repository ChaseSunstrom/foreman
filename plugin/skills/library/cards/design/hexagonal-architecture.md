---
name: hexagonal-architecture
title: Hexagonal architecture
area: design
tags: [hexagonal, ports-adapters, clean-architecture, domain, boundaries, testing]
detect: []
related: [domain-driven-design, dependency-injection, modular-monolith, error-handling]
---
Ports and adapters: the domain depends on nothing, and I/O sits behind interfaces the core owns.

## Verify
- `grep -rnE "^(import|from) .*(sqlalchemy|django|fastapi|requests|boto3)" src/domain src/application`: no framework or I/O imports in the core (expect no output; adjust package names).
- `pytest -q tests/domain tests/application`: core tests run with fakes and no network or DB.
- `npx dependency-cruiser --validate .dependency-cruiser.js src`: layer rules hold in a JS or TS repo with that config.
- `go list -deps ./internal/domain/... | grep -E "database/sql|net/http"`: the domain package does not pull in I/O packages (expect no output).

## Test first
Test the use case through its inbound port with in-memory adapters.
```python
class FakeOrders(OrderRepo):
    def __init__(self): self.rows = {}
    def save(self, o): self.rows[o.id] = o
    def get(self, id): return self.rows.get(id)

def test_place_order_saves_and_publishes():
    repo, bus = FakeOrders(), FakeBus()
    PlaceOrder(repo, bus)(sku="A1", qty=2)
    assert len(repo.rows) == 1 and bus.published[0].type == "OrderPlaced"
```

## Do
- Layers: domain (entities, value objects, rules), application (use cases, port interfaces), adapters (HTTP, DB, queues). Dependencies point inward only.
- Define outbound ports (`OrderRepo`, `Clock`, `PaymentGateway`) in the core, in the core's vocabulary. Adapters implement them.
- Make each use case one class or function taking its ports as constructor arguments. Wire everything in one composition root.
- Map between layers explicitly: DTO to command, entity to row. Do not pass ORM models or request objects inward.
- Keep inbound adapters thin: parse, call the use case, map errors to protocol codes.
- Test each adapter against the real dependency with a contract test (a shared suite run against fake and real).
- Inject time and IDs through ports, so tests are deterministic.

## Avoid
- Domain entities that inherit from ORM base classes or carry framework decorators: the core can't be tested or moved without the framework. Map at the edge.
- Port interfaces shaped like the library API (`execute_sql`): leaks the adapter. Name by intent (`find_overdue_invoices`).
- An interface for everything with a single implementation: add ports only at real I/O boundaries.
- Business rules in controllers or repositories: move them into entities or use cases.
- A fake that diverges from the real adapter: run the same contract tests against both.
- Service locators or global singletons inside the core: pass dependencies in.
- Letting adapters call each other (HTTP handler to DB): go through the use case.

## Review
- [ ] No imports of frameworks or drivers from the domain and application layers, enforced by a check.
- [ ] Each outbound dependency is a port defined by the core, with an in-memory fake.
- [ ] Adapters have integration or contract tests against the real thing.
- [ ] One composition root wires all dependencies.
- [ ] Errors are domain types, mapped to protocol codes only at the edge.
