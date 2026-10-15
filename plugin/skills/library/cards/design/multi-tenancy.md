---
name: multi-tenancy
title: Multi-tenancy
area: design
tags: [multi-tenancy, saas, isolation, row-level-security, authorization, tenants]
detect: [dep:django-tenants, dep:django-tenant-schemas, dep:acts_as_tenant, dep:apartment, dep:Finbuckle.MultiTenant]
related: [caching, background-jobs, error-handling, configuration, zero-downtime-migrations]
---
Many customers on shared infrastructure with isolation enforced in the data layer, not by remembering a WHERE clause.

## Verify
- `psql -c "select relname, relrowsecurity, relforcerowsecurity from pg_class where relname in ('orders','invoices')"`: row-level security is enabled (and forced) on tenant tables (Postgres RLS).
- `psql -c "select table_name from information_schema.columns where column_name='tenant_id'"`: the list of tenant-scoped tables matches the design.
- `pytest -q tests/isolation`: tenant A can't read, write or enumerate tenant B's data through any endpoint.
- `grep -rnE "\.(objects|query)\.(all|get|filter)" src | grep -v tenant`: queries bypassing tenant scoping are surfaced for review.

## Test first
Create two tenants and attack across the boundary.
```python
def test_tenant_cannot_read_other_tenants_order(client, tenant_a, tenant_b):
    order = create_order(tenant=tenant_b)
    r = client.get(f"/orders/{order.id}", headers=auth(tenant_a))
    assert r.status_code == 404          # not 403: do not confirm existence

def test_list_is_scoped(client, tenant_a, tenant_b):
    create_order(tenant=tenant_a); create_order(tenant=tenant_b)
    assert len(client.get("/orders", headers=auth(tenant_a)).json()["items"]) == 1
```

## Do
- Pick the isolation model deliberately: shared tables with `tenant_id`, schema per tenant, or database per tenant. Document the tradeoff.
- Resolve the tenant once per request from the authenticated identity (token claim, not a client-chosen header), and put it in request context.
- Enforce scoping below application code: Postgres RLS with `SET LOCAL app.tenant_id`, or a repository layer that always applies the filter.
- Make `tenant_id` part of unique constraints and composite indexes (`unique (tenant_id, email)`), and part of foreign keys.
- Include the tenant in cache keys, job payloads, file paths, search indexes and event metadata.
- Return 404 for another tenant's resource IDs.
- Test isolation as its own suite, on every endpoint and every background job.
- Add per-tenant rate limits and quotas, so one tenant can't starve others.

## Avoid
- Relying on every developer to add `.filter(tenant=...)`: one miss leaks data. Enforce it by default in the data layer.
- Tenant ID taken from a request header or body: a user can set another's. Derive it from the session.
- RLS with connection pooling that doesn't reset the setting: the next request inherits the previous tenant. Use `SET LOCAL` inside a transaction.
- Global unique indexes on tenant data (such as email): they leak existence across tenants and block valid signups. Scope them to the tenant.
- Cache keys, S3 paths or search indexes without a tenant prefix: cross-tenant reads. Namespace them.
- Superuser or table-owner DB roles for the app: they bypass RLS unless it is forced. Use a restricted role.
- Background jobs that load by ID with no tenant context: set it explicitly in the job.

## Review
- [ ] Tenant is derived from authentication and enforced at the data layer.
- [ ] Unique constraints and indexes include the tenant.
- [ ] Caches, queues, files and search are tenant-namespaced.
- [ ] An isolation test suite covers each endpoint and job.
- [ ] The app's DB role cannot bypass row-level security.
