---
name: diesel
title: Diesel
area: rust
tags: [rust, orm, sql, diesel, migrations, postgres]
detect: [dep:diesel, dep:diesel_migrations, dep:diesel-async, file:diesel.toml]
related: [sqlx, sea-orm, tokio, thiserror-anyhow]
---
Diesel ORM: schema.rs from migrations, typed queries, explicit transactions, async via diesel-async.

## Verify
- `diesel migration run`: migrations apply to the dev database.
- `diesel migration redo`: the latest `down.sql` really reverses `up.sql`.
- `diesel print-schema | diff - src/schema.rs`: committed schema matches the database.
- `cargo test`: tests run against a real database.
- `cargo clippy --all-targets -- -D warnings`: lints.

## Test first
Use `Connection::test_transaction` (or `begin_test_transaction`) so each test rolls back.
```rust
#[test]
fn duplicate_email_is_unique_violation() {
    let mut conn = test_conn();
    conn.test_transaction::<_, diesel::result::Error, _>(|conn| {
        create_user(conn, "a@x.io").unwrap();
        let err = create_user(conn, "a@x.io").unwrap_err();
        assert!(matches!(err, diesel::result::Error::DatabaseError(
            diesel::result::DatabaseErrorKind::UniqueViolation, _)));
        Ok(())
    });
}
```

## Do
- Write every schema change as a migration with a working `down.sql`; regenerate `schema.rs` via `diesel.toml` `print_schema`.
- Separate `Queryable`/`Selectable` read structs from `Insertable` write structs; select with `.select(User::as_select())`.
- Use `.get_result`, `.first`, `.load`, `.execute` deliberately, and `.optional()` for maybe-missing rows.
- Group multi-statement work in `conn.transaction(|conn| { ... })`.
- Pool with `r2d2` (sync) or `deadpool`/`bb8` with `diesel-async`; never share one connection across threads.
- Run embedded migrations at startup with `embed_migrations!` and `run_pending_migrations`.
- Add `.on_conflict(...)` for upserts and index the columns you filter on.

## Avoid
- Sync diesel calls inside async handlers: blocks the executor. Use `diesel-async` or `spawn_blocking`.
- Hand-editing `schema.rs`: overwritten on next print. Change the migration.
- `sql_query` with `format!`: SQL injection. Use `.bind::<Type, _>(..)`.
- Missing `down.sql`: rollbacks impossible. Write and redo-test it.
- `.load` then filter in Rust: pulls the table. Filter in the query.
- Field order mismatch in `Queryable` structs: runtime type errors. Use `Selectable` and `as_select()`.

## Review
- [ ] Each migration has up and down, and `redo` passes.
- [ ] `schema.rs` is generated and matches the database.
- [ ] No sync DB calls on async executors.
- [ ] Multi-step writes sit in one transaction; unique violations map to domain errors.
- [ ] No raw SQL built by string formatting.
