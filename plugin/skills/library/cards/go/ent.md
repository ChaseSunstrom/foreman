---
name: ent
title: ent (Go entity framework)
area: go
tags: [go, orm, ent, graph, codegen, migrations]
detect: [dep:entgo.io/ent, file:ent/schema/*.go]
related: [pgx, sqlc, gorm, go-context]
---
ent ORM: schemas in Go, code generation, typed queries with eager loading, transactions, and versioned migrations.

## Verify
- `go generate ./ent`: regenerates the client from `ent/schema`; the diff should only show intended changes.
- `go build ./... && go vet ./...`: the generated code compiles.
- `go test -race ./...`: tests run against SQLite in memory or a real database.
- `atlas migrate diff NAME --env local` (when Atlas versioned migrations are in use): produces the migration file for review.
- `git diff --exit-code ent`: committed generated code is current after generate.

## Test first
Enable the in-memory client and assert a constraint.
```go
func TestUniqueEmail(t *testing.T) {
	c := enttest.Open(t, "sqlite3", "file:ent?mode=memory&cache=shared&_fk=1")
	defer c.Close()
	ctx := context.Background()
	c.User.Create().SetEmail("a@x.io").SaveX(ctx)
	_, err := c.User.Create().SetEmail("a@x.io").Save(ctx)
	if !ent.IsConstraintError(err) {
		t.Fatalf("want constraint error, got %v", err)
	}
}
```

## Do
- Define fields, edges and indexes in `ent/schema/*.go`; run `go generate ./ent` after every change and commit the output.
- Add validators and `Unique()`, `Immutable()`, `Default` on fields; add indexes on filtered columns.
- Eager-load edges with `.WithPosts()` or `.WithOwner()` to avoid N+1.
- Use `client.Tx(ctx)` with `defer` rollback and `tx.Commit()`; wrap with a helper that rolls back on panic.
- Use `Query().Only(ctx)`, `First`, `All`, `Exist`, `Count` appropriately and test `ent.IsNotFound(err)`.
- Use versioned migrations (Atlas) for production; reserve `Schema.Create` auto-migration for dev and tests.
- Pass `ctx` to every call; use hooks and interceptors for cross-cutting concerns such as audit or soft delete.
- Use `entc` extensions or feature flags (for example `sql/upsert`) through `entc.go` configuration, and keep the generate directive consistent.

## Avoid
- Hand-editing generated files: overwritten. Change the schema.
- Auto-migrating in production: unreviewed destructive changes. Use versioned migrations and review SQL.
- Lazy per-row edge queries in loops: N+1. Eager-load.
- Forgetting `_fk=1` on SQLite tests: foreign keys not enforced, so tests pass where production fails.
- Ignoring `ent.IsConstraintError` and `ent.IsNotFound`: leaking raw errors. Map to domain errors.
- Checking in a stale generated client: builds on CI differ. Verify `git diff --exit-code`.
- Mismatched `entgo.io/ent` module and generator versions: confusing compile errors. Pin them together.

## Review
- [ ] Generated code is current and committed per team convention.
- [ ] Production schema changes come from reviewed versioned migrations.
- [ ] No N+1: edges are eager-loaded in list paths.
- [ ] Transactions roll back on error and commit explicitly.
- [ ] Constraint and not-found errors are mapped to domain errors.
