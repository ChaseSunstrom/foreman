---
name: postgres-rls
title: PostgreSQL row-level security
area: data
tags: [postgres, rls, security, multi-tenant, policies, supabase]
detect: []
related: [postgres, supabase, pgbouncer, postgres-indexes]
---
Row-level security for tenant isolation: policies, forced RLS, and the owner and BYPASSRLS traps.

## Verify
- `psql -c "SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname = 'invoices'"`: RLS enabled and forced.
- `psql -c "SELECT policyname, cmd, qual, with_check FROM pg_policies WHERE tablename = 'invoices'"`: policies per command, with a WITH CHECK on writes.
- `psql -c "SELECT rolname, rolbypassrls, rolsuper FROM pg_roles WHERE rolname = current_user"`: the app role bypasses nothing.
- `psql -c "EXPLAIN SELECT * FROM invoices"`: the policy filter is in the plan and uses an index.

## Test first
Connect as the app role, not the owner; set the tenant and prove isolation.
```python
def test_tenant_cannot_read_or_write_other(app_conn):
    app_conn.execute("SELECT set_config('app.tenant', 'A', false)")
    assert app_conn.execute("SELECT count(*) FROM invoices WHERE tenant_id='B'").fetchone()[0] == 0
    with pytest.raises(Exception):
        app_conn.execute("INSERT INTO invoices(tenant_id) VALUES ('B')")
```

## Do
- `ALTER TABLE t ENABLE ROW LEVEL SECURITY; ALTER TABLE t FORCE ROW LEVEL SECURITY;` so even the owner is filtered.
- `CREATE POLICY tenant ON t USING (tenant_id = current_setting('app.tenant')) WITH CHECK (tenant_id = current_setting('app.tenant'))`.
- Set the tenant per transaction with `SET LOCAL` or `set_config(..., true)`.
- Run the app as a dedicated role that is neither owner, superuser nor `BYPASSRLS`.
- Index the policy column and lead composite indexes with it.
- Write separate policies per command when read and write rules differ.
- Wrap function calls in policies as `(SELECT current_setting('app.tenant'))` so they evaluate once per query.

## Avoid
- Testing as the table owner or a superuser: RLS is silently skipped. Test as the app role.
- `USING` without `WITH CHECK` on INSERT and UPDATE: users can write rows they cannot read. Add WITH CHECK.
- Session-level `SET` behind a transaction pooler: the tenant leaks to the next client. Use `SET LOCAL` in a transaction.
- Forgetting views: they run with the view owner's rights and bypass RLS unless `security_invoker = true`.
- Policies that subquery other RLS tables heavily: slow plans and recursion. Denormalize `tenant_id`.
- Relying on RLS alone with no tenant column default or NOT NULL: add the constraint.

## Review
- [ ] Every tenant table has RLS enabled and forced.
- [ ] Policies have USING and WITH CHECK where needed.
- [ ] App role is non-owner, no BYPASSRLS.
- [ ] Tenant context is transaction-scoped.
- [ ] Isolation tests run as the app role.
