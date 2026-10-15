---
name: modular-monolith
title: Modular monolith
area: design
tags: [monolith, modules, boundaries, architecture, domain, coupling]
detect: []
related: [domain-driven-design, hexagonal-architecture, microservices, monorepo, dependency-injection]
---
One deployable divided into modules with owned data, public APIs and enforced boundaries, ready to extract later.

## Verify
- `npx dependency-cruiser --validate .dependency-cruiser.js src`: module boundary rules hold (JS or TS with a config).
- `python -m import_linter` (or `lint-imports`): import contracts pass (Python with `.importlinter`).
- `go vet ./... && go build ./...`: `internal/` packages block outside imports (Go).
- `grep -rnE "FROM (billing|shipping)_" src/orders`: no module reads another module's tables (expect no output; adjust prefixes).

## Test first
Fail the build on a boundary violation, then fix the code.
```ini
# .importlinter
[importlinter]
root_package = shop

[importlinter:contract:orders-no-billing-internals]
name = orders only uses billing's public API
type = forbidden
source_modules = shop.orders
forbidden_modules = shop.billing.internal
```
Run `lint-imports`; it fails until `orders` calls `shop.billing.api` instead.

## Do
- Give each module a public API file (`api.py`, `index.ts`, an exported interface) and keep the rest private.
- Let each module own its tables. Other modules get data through the API or published events, not joins.
- Communicate through function calls to the public API for queries, and in-process events for reactions.
- Use IDs, not object references or foreign keys, across module boundaries.
- Keep one database but separate schemas or table prefixes per module, with the rule written down.
- Enforce rules in CI with an import-linter tool. A convention alone decays.
- Give modules their own tests that run without the others, using their API fakes.
- Extract a module to a service only when scale, team or release cadence demands it. The API is already the seam.

## Avoid
- Cross-module SQL joins and shared ORM models: the modules become a tangle that can't be separated. Call the API and copy what you need.
- A `common` or `shared` module that grows domain logic: keep it to truly generic code.
- Circular dependencies between modules: introduce an event or move the shared concept to a third module.
- Boundaries that exist only in folder names: add automated import checks.
- A transaction spanning several modules by habit: it welds them together. Keep each transaction inside one module, and use events for the rest.
- Premature microservice extraction: distribution costs, so prove the need.

## Review
- [ ] Each module exposes a small public API, and boundary checks run in CI.
- [ ] No module imports another's internals or reads its tables.
- [ ] Cross-module references use IDs.
- [ ] Module tests run in isolation with fakes of other modules.
- [ ] Cycles are absent in the dependency graph.
