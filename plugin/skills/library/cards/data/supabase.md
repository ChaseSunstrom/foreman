---
name: supabase
title: Supabase
area: data
tags: [supabase, postgres, auth, rls, storage, realtime]
detect: [dep:@supabase/supabase-js, dep:supabase, dep:@supabase/ssr, dep:supabase-py, dep:supabase-flutter, dep:supabase-community/supabase-go, file:supabase/config.toml]
related: [postgres, sql-migrations, firebase, pgvector]
---
Supabase: Postgres with row-level security, auth, storage and realtime; the client key decides who you are.

## Verify
- `supabase db lint`: schema lint against the local database.
- `supabase db reset`: all migrations and `seed.sql` apply cleanly from scratch.
- `supabase test db`: pgTAP tests in `supabase/tests` pass.
- `supabase db diff`: the local schema matches committed migrations (no drift).
- `supabase migration list`: local and remote migration history agree.

## Test first
Write a pgTAP test showing an anonymous or other-tenant user cannot read a row.
```sql
begin;
select plan(1);
set local role authenticated;
select set_config('request.jwt.claims', '{"sub":"user-b"}', true);
select is_empty($$select * from notes where owner = 'user-a'$$, 'RLS hides other users rows');
select * from finish();
rollback;
```
Fails until RLS is enabled with an owner policy.

## Do
- Enable RLS on every table in an exposed schema (`alter table t enable row level security`) and write explicit policies per command with `using` and `with check`.
- Reference the user as `(select auth.uid())` in policies so it evaluates once per query.
- Index columns used in policies.
- Make schema changes as migrations (`supabase migration new`), and push with `supabase db push`.
- Use the anon key in browsers; keep the `service_role` key on trusted servers only.
- Use `@supabase/ssr` helpers for cookie-based sessions in server frameworks.
- Generate types with `supabase gen types typescript` and rerun after schema changes.
- Set storage bucket policies and use signed URLs for private files.

## Avoid
- A table without RLS in the `public` schema: the API exposes it to anyone with the anon key. Enable RLS and add policies.
- Shipping the `service_role` key in client code or `NEXT_PUBLIC_` variables: bypasses RLS. Server only.
- Trusting `user_metadata` in policies: users can edit it. Use `app_metadata` or a roles table.
- `getSession()` for server-side authorization: reads an unverified cookie. Use `getUser()`.
- Policies calling `auth.uid()` bare on large tables: per-row evaluation. Wrap in `select`.
- Editing the schema in the dashboard only: drift from migrations. Capture with `db diff`.
- `security definer` functions without a fixed `search_path`: privilege escalation. Set `search_path = ''`.

## Review
- [ ] Every exposed table has RLS and a policy test.
- [ ] No service key reaches the client bundle.
- [ ] Policies use app-controlled claims and indexed columns.
- [ ] Migrations are committed and `db reset` succeeds.
- [ ] Generated types are current.
