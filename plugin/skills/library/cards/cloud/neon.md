---
name: neon
title: Neon Postgres
area: cloud
tags: [neon, postgres, serverless, branching, pooling, database]
detect: [dep:@neondatabase/serverless, dep:neonctl, dep:@neondatabase/api-client]
related: [aws-rds, gcp-cloud-sql, vercel, cloudflare-workers]
---
Neon serverless Postgres: a pooled connection string for apps, a direct one for migrations, a branch per preview or test, and cold-start-aware clients.

## Verify
- `neonctl projects list`: the CLI is authenticated and sees the project.
- `neonctl branches list --project-id P`: branches and their parents.
- `neonctl connection-string BRANCH --project-id P --pooled`: the pooled string (host contains `-pooler`) for app traffic.
- `psql "$DATABASE_URL" -c 'select 1'`: the string connects with TLS.
- `psql "$DIRECT_URL" -c 'show server_version'`: the direct string works for migrations.

## Test first
Run migrations and tests on a throwaway branch, never the main one.
```python
def test_migration_applies_cleanly_on_branch(branch_url):
    run(["alembic", "upgrade", "head"], env={"DATABASE_URL": branch_url})
    with connect(branch_url) as c:
        assert c.execute("select to_regclass('public.orders')").scalar() is not None
```

## Do
- Use the pooled connection string (PgBouncer in transaction mode) for application and serverless traffic, and the direct string for migrations, `pg_dump` and anything that needs session state.
- Create a branch per pull request or test run from the parent and delete it afterwards. Branches copy-on-write, so they are cheap.
- Use the serverless driver (`@neondatabase/serverless`) for edge runtimes and short-lived functions. Use ordinary drivers with a pool on long-running servers.
- Keep `sslmode=require` in connection strings and store them as secrets.
- Handle scale-to-zero cold starts with connection retry and a sensible connect timeout. Raise the minimum compute or disable suspend for latency-critical production.
- Set autoscaling min and max compute and a history retention window that covers your restore needs, and rehearse a point-in-time restore through a branch.
- Create a least-privilege role for the app and keep the owner role for migrations.
- Pin the Postgres major version in the project settings and test upgrades on a branch.

## Avoid
- The direct connection from many serverless invocations: connection limits fill up. Use the pooled string.
- Session features on the pooled endpoint (`SET` across statements, advisory locks, `LISTEN`, prepared statements in older setups): they break in transaction mode. Use the direct string for those.
- Running migrations against the pooled string: DDL and session settings can misbehave. Use direct.
- Tests against the production branch: they mutate real data. Branch from it.
- Leaving old branches around: they accrue storage and compute. Delete them in CI cleanup.
- Passwords in the repo or in client bundles: keep in secrets and call the database from the server.
- Assuming zero cold start: the first query after idle can be slow. Retry and set timeouts.

## Review
- [ ] App uses the pooled string, migrations use the direct string.
- [ ] CI creates and deletes a branch for tests and previews.
- [ ] The app role has minimal privileges, and TLS is required.
- [ ] Cold start and retry behavior are handled.
- [ ] Retention and restore procedure are known.
