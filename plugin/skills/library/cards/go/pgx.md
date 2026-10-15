---
name: pgx
title: pgx (PostgreSQL driver)
area: go
tags: [go, postgres, pgx, pgxpool, sql, transactions]
detect: [dep:github.com/jackc/pgx/v5, dep:github.com/jackc/pgx/v5/pgxpool]
related: [sqlc, go-context, go-errors, gorm]
---
pgx v5 with pgxpool: parameterized queries, scanning helpers, transactions, pool config and error codes.

## Verify
- `go vet ./...`: lints.
- `go test -race ./...`: tests run against a real Postgres (container or local), not a mock.
- `psql "$DATABASE_URL" -c "select 1"`: connectivity and credentials work.
- `go test -run TestMigrations ./...`: schema applies from scratch.

## Test first
Use a real database and assert the SQLSTATE.
```go
func TestInsertDuplicateEmail(t *testing.T) {
	pool := testPool(t)
	_, _ = pool.Exec(ctx, "insert into users(email) values($1)", "a@x.io")
	_, err := pool.Exec(ctx, "insert into users(email) values($1)", "a@x.io")
	var pe *pgconn.PgError
	if !errors.As(err, &pe) || pe.Code != "23505" {
		t.Fatalf("want unique violation, got %v", err)
	}
}
```

## Do
- Create one `pgxpool.New(ctx, dsn)` at startup (or `ParseConfig` then tune `MaxConns`, `MinConns`, `MaxConnLifetime`, `HealthCheckPeriod`), share it, `defer pool.Close()`.
- Pass values as `$1, $2` args; never concatenate.
- Scan with `pgx.CollectRows(rows, pgx.RowToStructByName[T])` and `pgx.CollectOneRow`; field names map to column names (use `db:"col"` tags).
- Handle absence with `errors.Is(err, pgx.ErrNoRows)`.
- Transactions: `tx, _ := pool.Begin(ctx)`, `defer tx.Rollback(ctx)`, then `tx.Commit(ctx)`; or `pgx.BeginTxFunc`.
- Batch round trips with `pgx.Batch` and `pool.SendBatch`; bulk-load with `CopyFrom`.
- Detect constraint failures through `*pgconn.PgError` `.Code` and `.ConstraintName`.
- Pass `ctx` with timeouts into every call.

## Avoid
- `fmt.Sprintf` into SQL: injection. Use placeholders (identifiers need a whitelist or `pgx.Identifier{...}.Sanitize()`).
- Forgetting `rows.Close()` or iterating without checking `rows.Err()`: connection leaks, missed errors. `CollectRows` handles both.
- Holding a `pool.Acquire` conn without `Release`: pool starvation. `defer conn.Release()`.
- Using a single `pgx.Conn` across goroutines: not safe. Use the pool.
- Importing the v4 path (`github.com/jackc/pgx/v4`): old API. Use `/v5`.
- Comparing `err == pgx.ErrNoRows`: wrapped errors miss. Use `errors.Is`.
- Ignoring PgBouncer transaction mode: prepared statement cache breaks. Set `QueryExecModeExec` or `QueryExecModeSimpleProtocol` in config.

## Review
- [ ] One shared pool, closed on shutdown, sized deliberately.
- [ ] All queries parameterized; every connection or row set is released.
- [ ] Transactions have a deferred rollback and explicit commit.
- [ ] Constraint errors map to domain errors via SQLSTATE.
- [ ] Tests hit a real Postgres.
