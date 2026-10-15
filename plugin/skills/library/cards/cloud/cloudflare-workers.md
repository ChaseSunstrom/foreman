---
name: cloudflare-workers
title: Cloudflare Workers
area: cloud
tags: [cloudflare, workers, edge, wrangler, serverless, bindings]
detect: [dep:wrangler, dep:@cloudflare/workers-types, dep:@cloudflare/vitest-pool-workers, file:wrangler.toml, file:wrangler.json, file:wrangler.jsonc]
related: [cloudflare-d1-r2, vercel, netlify]
---
Cloudflare Workers: fetch handlers on the V8 isolate runtime, resource bindings in the wrangler config, local dev with wrangler.

## Verify
- `npx wrangler types`: generates `Env` types from the bindings in the config.
- `npx tsc --noEmit`: handlers and bindings type-check.
- `npx wrangler deploy --dry-run --outdir dist`: the bundle builds and the config is valid without publishing.
- `npx wrangler dev`: runs locally against local binding state.
- `npx vitest run`: tests pass inside the Workers runtime.

## Test first
Use the Workers Vitest pool so tests run in workerd with real bindings.
```typescript
import { SELF } from "cloudflare:test";
import { it, expect } from "vitest";

it("rejects unauthenticated writes", async () => {
  const res = await SELF.fetch("https://x/api/items", { method: "POST", body: "{}" });
  expect(res.status).toBe(401);
});
```
Tests live in `test/`; configure `defineWorkersConfig` with `poolOptions.workers.wrangler.configPath`.

## Do
- Declare bindings (KV, D1, R2, Queues, Durable Objects, `vars`) in the wrangler config; read them from `env`, not globals.
- Set `compatibility_date` to a recent date you tested, and add `compatibility_flags = ["nodejs_compat"]` only if you need Node APIs.
- Keep secrets out of the config: `wrangler secret put NAME`, and `.dev.vars` (gitignored) locally.
- Use `ctx.waitUntil(promise)` for work after the response, such as logging.
- Stream large bodies; do not buffer them. Use the Cache API or `cf` fetch options for caching.
- Use Durable Objects for coordination or per-key state; KV is eventually consistent.
- Use `[env.staging]` sections with separate bindings per environment.
- Return `Response` objects from every path, including errors.

## Avoid
- Module-level mutable state to share data between requests: isolates are reused or recreated unpredictably. Use KV, D1 or Durable Objects.
- The old Service Worker syntax (`addEventListener("fetch")`): use `export default { fetch(req, env, ctx) {} }`.
- Floating promises with no `waitUntil`: work is cancelled once the response ends.
- Assuming Node built-ins without `nodejs_compat`: imports fail at bundle time.
- Secrets in `[vars]`: they are visible in the dashboard and the repo.
- Long CPU loops: CPU time is limited per request; offload to Queues or Workflows.
- Treating KV as read-after-write consistent.

## Review
- [ ] Bindings declared in config and typed via `wrangler types`.
- [ ] Secrets set with `wrangler secret`, none in `vars`.
- [ ] Background work uses `waitUntil`.
- [ ] `compatibility_date` and flags are intentional.
- [ ] Staging and production use separate bindings.
