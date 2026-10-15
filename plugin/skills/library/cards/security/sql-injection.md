---
name: sql-injection
title: SQL injection
area: security
tags: [security, sql, injection, database, orm, parameterized]
detect: [dep:sqlalchemy, dep:psycopg2, dep:psycopg, dep:mysqlclient, dep:pg, dep:mysql2, dep:sequelize, dep:knex, dep:github.com/jackc/pgx/v5, dep:sqlx]
related: [input-validation, owasp-top-10, semgrep, authorization]
---
SQL injection: bind every value as a parameter, allowlist identifiers, and prove it with a payload test.

## Verify
- `semgrep scan --config p/sql-injection --error`: no string-built queries remain.
- `grep -rnE "(execute|query|raw)\(f?[\"'].*(\+|%s|\{|\\$\{)" src/`: no concatenated or interpolated query strings.
- `pytest -q tests/security/test_sqli.py`: payloads return data as literals, not extra rows or errors.

## Test first
```python
import pytest
PAYLOADS = ["' OR '1'='1", "'; DROP TABLE users;--", "1 UNION SELECT password FROM users--"]

@pytest.mark.parametrize("p", PAYLOADS)
def test_search_treats_input_as_literal(client, seeded_users, p):
    r = client.get("/users", params={"name": p})
    assert r.status_code == 200 and r.json() == []
    assert User.count() == len(seeded_users)
```

## Do
- Use placeholders for every value: `cur.execute("SELECT * FROM u WHERE id = %s", (uid,))`, `$1` in pg, `?` in sqlite and MySQL, SQLAlchemy `text("... :id")` with `.bindparams` or Core expressions.
- Allowlist identifiers you must vary (sort column, table): map user input to a fixed dict of known names.
- For `IN` lists generate the placeholders from the length, and bind each element.
- Use an ORM or query builder for the common path, and keep raw SQL in a few reviewed functions.
- Connect with a least-privilege database role: no DDL, no access to other schemas.
- Cap `LIMIT` and validate numeric types before they reach the query.
- Return generic errors; log the database error server-side only.

## Avoid
- f-strings, `%` formatting or `+` to build SQL: that is the injection. Pass parameters separately.
- Believing the ORM is always safe: `.raw()`, `text(f"...")`, `extra()`, `literal_column(user)`, Sequelize `query` with interpolation, and Knex `whereRaw` with concatenation all inject. Bind with `?` or named params.
- Escaping quotes by hand (`replace("'", "''")`): encoding and multibyte bugs defeat it. Use binds.
- Parameterizing identifiers (`ORDER BY %s`): drivers quote them as strings and break or leave the hole. Allowlist instead.
- A privileged app database user: one injection becomes full takeover. Restrict the role.
- Detailed SQL errors in responses: they teach the attacker the schema. Return a generic message.

## Review
- [ ] No query is built from user data by string operations.
- [ ] Dynamic identifiers go through an allowlist.
- [ ] Raw SQL escape hatches in the ORM were checked.
- [ ] The database role is least-privilege.
- [ ] A payload test covers each new query that takes input.
