---
name: sqlx
title: SQLx
area: rust
tags: [rust, database, sql, sqlx, async, migrations]
detect: [dep:sqlx, file:.sqlx/*, file:migrations/*.sql]
related: [tokio, axum, serde, cargo]
---
SQLx: async SQL with compile-time checked queries, migrations, pooling and transactions.

## Verify
- `cargo sqlx prepare --check`: the committed `.sqlx` offline data matches the queries (needs sqlx-cli and a DATABASE_URL).
- `sqlx migrate run`: migrations apply cleanly to a scratch database.
- `SQLX_OFFLINE=true cargo check --all-targets`: builds without a live database, as CI will.
- `cargo test`: including `#[sqlx::test]` database tests.

## Test first
`#[sqlx::test]` gives each test its own fresh database with migrations applied.
```rust
#[sqlx::test]
async fn duplicate_email_is_rejected(pool: sqlx::PgPool) {
    sqlx::query!("INSERT INTO users (email) VALUES ($1)", "a@b.c")
        .execute(&pool).await.unwrap();
    let err = sqlx::query!("INSERT INTO users (email) VALUES ($1)", "a@b.c")
        .execute(&pool).await.unwrap_err();
    assert!(err.as_database_error().unwrap().is_unique_violation());
}
```
Needs `DATABASE_URL` in the environment. Put migrations in `migrations/`.

## Do
- Use `sqlx::query!`, `query_as!` and `migrate!` so SQL is checked at compile time. Run `cargo sqlx prepare` and commit `.sqlx`.
- Select one runtime and TLS feature pair, for example `runtime-tokio` with `tls-rustls`, and the one database feature you use.
- Share one `PgPool` (or the matching pool) in application state with `PgPoolOptions::new().max_connections(n)`.
- Wrap multi-statement changes in `pool.begin()` and `tx.commit()`. A dropped transaction rolls back.
- Write forward-only, timestamp-ordered migrations and never edit an applied one.
- Derive `FromRow` for dynamic `query_as` and use `fetch_optional` where zero rows is valid.
- Use `QueryBuilder::push_bind` for dynamic SQL.

## Avoid
- Building SQL with `format!` and user input: injection. Bind with `$1` or `?`.
- Forgetting to commit offline data: CI fails with a missing `DATABASE_URL`. Run `cargo sqlx prepare` after query changes.
- Editing a migration that has already run: a checksum mismatch error. Add a new migration.
- `fetch_one` where a row may be missing: it returns `RowNotFound`. Use `fetch_optional`.
- A new pool per request: connection exhaustion. Share one.
- Holding a transaction open across slow external calls: it pins a connection and locks.
- Unreviewed nullable mapping: `query!` infers `Option` from the schema, so override with `"col!"` only when certain.

## Review
- [ ] All queries use bound parameters.
- [ ] `.sqlx` data is up to date and migrations are new files only.
- [ ] Transactions cover every multi-step write.
- [ ] Unique, foreign-key and not-null constraints exist in the schema, not only in code.
- [ ] Pool size and acquire timeouts are set deliberately.
