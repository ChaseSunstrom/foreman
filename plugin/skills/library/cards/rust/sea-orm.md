---
name: sea-orm
title: SeaORM
area: rust
tags: [rust, orm, sql, sea-orm, migrations, async]
detect: [dep:sea-orm, dep:sea-orm-migration]
related: [sqlx, diesel, tokio, axum]
---
SeaORM async ORM: entities, ActiveModel writes, relations without N+1, migrations in Rust.

## Verify
- `sea-orm-cli migrate up`: migrations apply.
- `sea-orm-cli migrate down`: the last migration reverses cleanly (then `up` again).
- `sea-orm-cli generate entity -o src/entities`: entities regenerate; `git diff --stat src/entities` shows only intended drift.
- `cargo test`: tests run against SQLite in memory or a real test database.
- `cargo clippy --all-targets -- -D warnings`: lints.

## Test first
In-memory SQLite with the migrator applied.
```rust
#[tokio::test]
async fn insert_then_find() {
    let db = Database::connect("sqlite::memory:").await.unwrap();
    Migrator::up(&db, None).await.unwrap();
    let m = user::ActiveModel { name: Set("ann".into()), ..Default::default() }
        .insert(&db).await.unwrap();
    assert_eq!(User::find_by_id(m.id).one(&db).await.unwrap().unwrap().name, "ann");
}
```

## Do
- Keep schema in the `migration` crate using `SchemaManager`; write `down` for every `up`.
- Write with `ActiveModel` and `Set(..)`; fields left `NotSet` are omitted from the insert.
- Fetch related rows with `find_with_related` or `find_also_related`, or `load_many`, not a query per row.
- Wrap multi-step writes in `db.begin().await?` ... `txn.commit().await?`, or `db.transaction(|txn| Box::pin(async move { .. }))`.
- Pass `&DatabaseConnection` (it is a pool and cheap to clone) or `&impl ConnectionTrait` so code works inside a transaction.
- Use `.paginate(db, page_size)` for large result sets, and `.into_model::<T>()` for partial selects.
- Set pool options with `ConnectOptions` (`max_connections`, `connect_timeout`, `sqlx_logging`).

## Avoid
- Per-row `find_related` in loops: N+1. Use `load_many` or joins.
- Updating through `Model` fields: models are immutable. Convert with `.into_active_model()` and `Set`.
- `ActiveModel::from(model).update()` with every field `Unchanged`: nothing is written. Set the changed fields.
- Forgetting `txn.commit()`: dropping rolls back silently. Commit explicitly.
- `Statement::from_string` with interpolated input: injection. Use `from_sql_and_values`.
- Editing generated entity files by hand: next generate overwrites. Put logic in separate impl blocks.

## Review
- [ ] Each migration has a tested `down`.
- [ ] No queries inside loops over results.
- [ ] Transactions commit explicitly and are passed through as `ConnectionTrait`.
- [ ] No raw SQL built from user input.
- [ ] Tests run the real migrator.
