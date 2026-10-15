---
name: cloudflare-d1-r2
title: Cloudflare D1 and R2
area: cloud
tags: [cloudflare, d1, r2, sqlite, object-storage, wrangler]
detect: [dep:wrangler, dep:@cloudflare/workers-types, dep:drizzle-orm, file:wrangler.toml, file:wrangler.jsonc, file:migrations/*.sql]
related: [cloudflare-workers, aws-s3]
---
Cloudflare D1 (SQLite) and R2 (S3-compatible objects) used through Worker bindings, with migrations and no egress surprises.

## Verify
- `npx wrangler d1 migrations list DB --local`: pending migrations against local state.
- `npx wrangler d1 migrations apply DB --local`: migrations apply cleanly to the local database.
- `npx wrangler d1 execute DB --local --command "select count(*) from items"`: the data is queryable.
- `npx wrangler r2 object get BUCKET/key --local --file out.bin`: a stored object round-trips locally.

## Test first
Run in the Workers Vitest pool, with bindings from the config.
```typescript
import { env } from "cloudflare:test";
import { it, expect } from "vitest";

it("stores and reads an object", async () => {
  await env.BUCKET.put("a.txt", "hi");
  const o = await env.BUCKET.get("a.txt");
  expect(await o!.text()).toBe("hi");
  const row = await env.DB.prepare("select 1 as n").first();
  expect(row).toEqual({ n: 1 });
});
```

## Do
- Bind D1 and R2 in the wrangler config (`[[d1_databases]]`, `[[r2_buckets]]`); use `env.DB` and `env.BUCKET`.
- Put schema changes in numbered files under `migrations/` and apply with `wrangler d1 migrations apply`.
- Use prepared statements with `.bind(...)`; use `db.batch([...])` for several statements in one round trip and one transaction.
- Add indexes for filtered columns; check with `EXPLAIN QUERY PLAN`.
- Pass `object.body` (a stream) straight into `new Response(...)` with `etag` and `httpEtag` headers.
- Use `put` with `httpMetadata.contentType` and `customMetadata`.
- Use presigned URLs through the S3-compatible API for direct browser uploads; scope the API token to one bucket.
- Use `list({ cursor, prefix })` and follow `truncated` for pagination.

## Avoid
- String-concatenated SQL: use `.bind()` to avoid injection.
- Forgetting `--local` or `--remote`: commands target different databases, and remote changes are real. State which you mean.
- Treating D1 as high-write OLTP: a database serialises writes; shard or batch.
- Reading `object.body` twice: a stream is consumed once. Use `.tee()` or re-fetch.
- Calling `get` and assuming non-null: it returns null for a missing key.
- Editing applied migration files: add a new one.
- Public bucket access when a Worker route with auth would do.

## Review
- [ ] Every query is parameterised and indexed.
- [ ] Migrations are new numbered files, applied locally first.
- [ ] Null returns from R2 and D1 handled.
- [ ] Streams are not read twice.
- [ ] Local vs remote targets are explicit in scripts.
