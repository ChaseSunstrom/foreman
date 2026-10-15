---
name: sqlc
title: sqlc
area: go
tags: [go, sql, sqlc, codegen, database, migrations]
detect: [file:sqlc.yaml, file:sqlc.yml, file:sqlc.json]
related: [go-testing, go-modules, gin, chi, echo]
---
sqlc: write SQL in files, generate type-safe Go, and keep the generated code in sync with the schema.

## Verify
- `sqlc generate`: regenerates Go from queries and schema (fails on invalid SQL or unknown columns).
- `sqlc vet`: runs configured query checks (needs rules in config).
- `git diff --exit-code -- db/`: generated code is committed and current (adjust the path to your `out` dir).
- `go build ./... && go test ./... -race`: callers compile and pass against the new signatures.

## Test first
Write the query and a test against a real database before generating.
```sql
-- name: GetUserByEmail :one
SELECT id, email FROM users WHERE email = $1;
```
```go
func TestGetUserByEmailMissing(t *testing.T) {
	q := db.New(testPool(t)) // pool on a scratch database with migrations applied
	_, err := q.GetUserByEmail(ctx, "nobody@x.y")
	if !errors.Is(err, pgx.ErrNoRows) {
		t.Fatalf("got %v", err)
	}
}
```
Queries live in `*.sql` files under the configured `queries` path. Run `sqlc generate` after each edit.

## Do
- Point `schema` at your migrations directory so sqlc and the database share one source of truth.
- Annotate each query: `:one`, `:many`, `:exec`, `:execrows` or `:batchexec`.
- Pick the driver in config (`sql_package: "pgx/v5"` for pgx) and match the `engine`.
- Use `sqlc.arg(name)` and `sqlc.narg(name)` for named and nullable parameters.
- Use `emit_interface: true` to mock the `Querier` in handler tests, and wrap writes in transactions with `q.WithTx(tx)`.
- Add `overrides` for types (UUID, numeric, JSON) once, in config.
- Commit generated files and regenerate in CI to catch drift.
- Pin the sqlc version in CI and in the generated file header.

## Avoid
- Editing generated `*.sql.go` files: they are overwritten. Change the SQL or config.
- `SELECT *` in queries: adding a column changes struct shape silently. List columns.
- Dynamic SQL via string concatenation outside sqlc: injection. Use `sqlc.narg` with `IS NULL OR` filters, or build a vetted query separately with bound args.
- Letting the schema in sqlc config drift from real migrations: queries compile but fail at runtime. Point both at the same files.
- Ignoring `pgx.ErrNoRows` or `sql.ErrNoRows` from `:one` queries: map to 404 or domain errors.
- Mixed `database/sql` and pgx native types after switching `sql_package`: regenerate and fix callers.
- Running migration tool statements sqlc can't parse (for example `-- +goose Down` sections): configure schema per tool, or keep schema files separate.

## Review
- [ ] Generated code is regenerated, committed and not hand-edited.
- [ ] Every query lists columns and uses bound parameters.
- [ ] `:one` callers handle the no-rows error.
- [ ] Type overrides are in config, not scattered casts.
- [ ] The schema source is shared with migrations.
