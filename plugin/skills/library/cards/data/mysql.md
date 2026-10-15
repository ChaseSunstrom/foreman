---
name: mysql
title: MySQL / MariaDB
area: data
tags: [sql, mysql, mariadb, database, innodb, indexes]
detect: [dep:mysqlclient, dep:PyMySQL, dep:aiomysql, dep:mysql2, dep:mysql, dep:go-sql-driver/mysql, dep:mysql-connector-java, dep:mariadb]
related: [sql-migrations, query-tuning, n-plus-one]
---
MySQL/MariaDB with InnoDB: utf8mb4, parameterized queries, short transactions, indexes proven by EXPLAIN.

## Verify
- `mysql -e "EXPLAIN FORMAT=TREE <query>"`: the plan the optimizer picks (MySQL 8).
- `mysql -e "EXPLAIN ANALYZE <query>"`: actual timings and row counts (MySQL 8.0.18+).
- `mysql -e "SHOW CREATE TABLE t\G"`: engine, charset, collation, keys as stored.
- `mysql -e "SELECT @@sql_mode, @@transaction_isolation"`: strict mode on and the isolation you assumed.

## Test first
Test against a real MySQL of the production major version. Assert the constraint before writing the migration.
```python
def test_duplicate_email_rejected(conn):
    conn.execute("insert into users(email) values ('a@x.io')")
    with pytest.raises(IntegrityError):
        conn.execute("insert into users(email) values ('a@x.io')")
```

## Do
- Use `utf8mb4` and a `utf8mb4_0900_ai_ci` or `utf8mb4_unicode_ci` collation on every table and connection.
- Keep strict `sql_mode` (`STRICT_TRANS_TABLES`, `ONLY_FULL_GROUP_BY`) so bad data errors instead of truncating.
- Use bind parameters (`%s` / `?`), never string interpolation.
- Index FK columns and order composite indexes by equality columns first, then range.
- Upsert with `INSERT ... ON DUPLICATE KEY UPDATE`; read affected rows to know which happened.
- Keep transactions short, take locks in a consistent order, and retry on deadlock (error 1213).
- Use online DDL (`ALGORITHM=INPLACE, LOCK=NONE`) or gh-ost/pt-osc for big tables.

## Avoid
- Legacy `utf8` (3-byte): drops emoji and breaks inserts. Use `utf8mb4`.
- Non-strict `sql_mode`: silent truncation and zero dates. Enable strict mode.
- Functions on indexed columns in `WHERE` (`DATE(created_at) = ...`): disables the index. Use a range.
- `OFFSET` deep pagination: scans skipped rows. Use keyset.
- Assuming `LIMIT` without `ORDER BY` is stable: add a deterministic order.
- Random UUIDv4 as clustered primary key: page splits and bloated secondaries. Use auto-increment or ordered UUIDs.
- MyISAM tables: no transactions or FKs. Use InnoDB.

## Review
- [ ] Charset and collation are utf8mb4 end to end, including the connection.
- [ ] All queries parameterized; no dynamic identifiers from user input.
- [ ] Migration avoids a long table lock on large tables.
- [ ] Deadlock retry exists around contended transactions.
- [ ] EXPLAIN shows an index for each new hot query.
