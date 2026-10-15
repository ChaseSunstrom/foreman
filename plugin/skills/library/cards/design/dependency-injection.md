---
name: dependency-injection
title: Dependency injection
area: design
tags: [dependency-injection, composition-root, testing, inversion, wiring, lifetimes]
detect: [dep:dependency-injector, dep:injector, dep:inversify, dep:tsyringe, dep:@nestjs/common, dep:google/wire, dep:uber.org/fx, dep:Microsoft.Extensions.DependencyInjection, dep:koin-core]
related: [hexagonal-architecture, configuration, concurrency, domain-driven-design]
---
Objects receive their collaborators instead of building them, wired once at a composition root, with explicit lifetimes.

## Verify
- `pytest -q`: units run with fakes injected, with no real network or DB.
- `grep -rnE "(requests|httpx|boto3)\.(get|post|client)\(" src/domain src/application`: core code doesn't construct I/O clients itself (expect no output).
- `go vet ./... && wire check ./...`: generated wiring is consistent (Go with Google Wire installed).
- `dotnet build -warnaserror`: missing registrations that analyzers catch fail the build (.NET).

## Test first
Swap a real dependency for a fake through the constructor.
```python
class FixedClock:
    def __init__(self, now): self._now = now
    def now(self): return self._now

def test_invoice_is_overdue_after_due_date():
    clock = FixedClock(datetime(2026, 2, 1))
    svc = InvoiceService(repo=InMemoryRepo(), clock=clock)
    inv = svc.create(due=datetime(2026, 1, 31))
    assert svc.is_overdue(inv.id) is True
```

## Do
- Prefer constructor injection. Dependencies are required, visible and immutable after construction.
- Depend on small interfaces the consumer defines (a `Clock`, `Mailer`, `Repo`), not on concrete classes.
- Build the object graph in one composition root (main, app factory, module file). Nothing else calls the container.
- Choose lifetimes on purpose: singleton for stateless or thread-safe clients and pools, scoped per request for sessions and unit-of-work, transient for cheap throwaways.
- Inject time, randomness and ID generation, so tests are deterministic.
- Use manual wiring until the graph is large. A framework container is optional, and plain functions or constructors work.
- Provide test overrides at the root (framework-style `dependency_overrides`, a test module), not by patching imports.
- Fail at startup when a registration is missing or the graph is circular.

## Avoid
- Service locator calls (`container.get(X)`) inside business code: dependencies become hidden and untestable. Inject through the constructor.
- A singleton that depends on a scoped service ("captive dependency"): the request-scoped object is held forever, and is shared between requests. Match or narrow lifetimes.
- Injecting the container itself: it is a locator in disguise.
- Constructors with more than about five dependencies: the class does too much. Split it.
- `mock.patch("module.global")` as the main test technique: it ties tests to import paths. Inject a fake.
- Module-level singletons created on import (`db = connect()`): they run at import time and are hard to replace. Create them in the root.
- Circular dependencies resolved by property injection: break the cycle by extracting an interface or an event.

## Review
- [ ] Core classes receive collaborators through constructors and own no I/O construction.
- [ ] One composition root builds the graph, and lifetimes are deliberate.
- [ ] Time, randomness and IDs are injectable.
- [ ] Tests use fakes or root-level overrides, with no import-path patching.
- [ ] No service locator calls in business code.
