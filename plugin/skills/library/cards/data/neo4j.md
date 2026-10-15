---
name: neo4j
title: Neo4j
area: data
tags: [neo4j, graph, cypher, constraints, indexes, bolt]
detect: [dep:neo4j, dep:neo4j-driver, dep:py2neo]
related: [data-modeling, query-tuning]
---
Neo4j graph databases with Cypher: modeling, constraints, parameterized queries, PROFILE and driver transaction functions.

## Verify
- `cypher-shell "PROFILE MATCH (u:User {email: $e}) RETURN u"`: plan shows NodeIndexSeek, not NodeByLabelScan, with db hits.
- `cypher-shell "SHOW CONSTRAINTS"`: uniqueness constraints exist.
- `cypher-shell "SHOW INDEXES"`: indexes are ONLINE.
- `cypher-shell "EXPLAIN <query>"`: plan without running it, to check for Eager or cartesian product operators.

## Test first
Use a throwaway database (testcontainers or an ephemeral instance), and assert on constraint behavior.
```python
def test_duplicate_email_rejected(session):
    session.run("CREATE CONSTRAINT user_email IF NOT EXISTS FOR (u:User) REQUIRE u.email IS UNIQUE")
    session.run("CREATE (:User {email: $e})", e="a@x.io")
    with pytest.raises(ConstraintError):
        session.run("CREATE (:User {email: $e})", e="a@x.io").consume()
```

## Do
- Model relationships as typed, directed edges with verbs (`(:User)-[:FOLLOWS]->(:User)`); put properties on the edge when it needs them.
- Create uniqueness constraints (which also create indexes) on the lookup keys before loading data.
- Always parameterize (`$param`); never concatenate values into Cypher.
- Use `MERGE` on the constrained key only, then `SET` other properties (`MERGE (u:User {id: $id}) SET u.name = $name`).
- Bound variable-length paths: `-[:KNOWS*1..4]->`.
- Use the driver's managed transactions (`execute_read` and `execute_write` in the Python driver) so transient failures retry.
- Batch loads with `UNWIND $rows AS row` instead of one query per row.
- Create one driver for the app lifetime and close it on shutdown; sessions are short-lived.

## Avoid
- Unbounded `[*]` path patterns: combinatorial explosion. Set limits.
- `MERGE` on a whole pattern with many properties: creates duplicates when one property differs. Merge on the key.
- Starting a MATCH without an indexed anchor: label scan over every node. Add an index or constraint.
- Very dense supernodes traversed without filtering: slow. Filter on relationship type and properties early, or model buckets.
- String-built Cypher: injection risk and no plan caching. Use parameters.
- A new driver per request: connection churn.
- Reading and writing in one retried function with side effects outside the database: the retry repeats them.

## Review
- [ ] Lookup properties have constraints or indexes (PROFILE shown).
- [ ] All queries parameterized.
- [ ] Variable-length patterns bounded.
- [ ] MERGE keys are constrained.
- [ ] Transaction functions are free of external side effects.
