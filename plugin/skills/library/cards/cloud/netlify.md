---
name: netlify
title: Netlify
area: cloud
tags: [netlify, deploy, functions, edge, redirects, jamstack]
detect: [dep:netlify-cli, dep:@netlify/functions, dep:@netlify/edge-functions, dep:@netlify/blobs, file:netlify.toml, file:_redirects, file:_headers]
related: [vercel, cloudflare-workers]
---
Netlify sites: `netlify.toml` build and routing, serverless and edge functions, deploy previews, per-context settings.

## Verify
- `npx netlify build`: runs the build as Netlify would, locally.
- `npx netlify dev`: serves the site, functions and redirects locally.
- `npx netlify deploy`: a draft deploy with a unique URL (no `--prod`).
- `npx netlify env:list`: environment variables and their scopes.
- `curl -sSI https://DRAFT_URL/old-path`: a redirect or header rule behaves as written.

## Test first
Assert routing and function behavior on the draft URL or via `netlify dev`.
```typescript
import { test, expect } from "vitest";

test("old path redirects permanently", async () => {
  const res = await fetch(`${process.env.SITE_URL}/old`, { redirect: "manual" });
  expect(res.status).toBe(301);
  expect(res.headers.get("location")).toBe("/new");
});
```
Test function handlers directly by calling the exported `handler` or default export with a `Request`.

## Do
- Declare `[build]` (`command`, `publish`, `functions`) and `[context.production]` or `[context.deploy-preview]` overrides in `netlify.toml`.
- Order redirects most specific first; rules match top to bottom and the first match wins. Use `force = true` to override an existing file.
- Write functions in `netlify/functions/`; export a default handler (modern) taking a `Request` and returning a `Response`.
- Add `[[headers]]` for security headers and long-lived cache on hashed assets.
- Set secrets in the UI or CLI, scoped to functions or builds; mark them secret.
- Use `[[redirects]]` with `status = 200` for rewrites and proxying; add an SPA fallback `/* /index.html 200` last.
- Pin the Node version with `NODE_VERSION` or `.nvmrc`.
- Use Netlify Blobs or an external store for data; functions are stateless.

## Avoid
- A catch-all `/*` SPA rule above specific rules: it shadows them.
- Secrets in `[build.environment]` of a committed `netlify.toml`: they land in the repo.
- Expecting the filesystem to persist between invocations or deploys.
- Functions that run beyond the synchronous timeout: use background functions (`-background` suffix) for long work.
- Deploying `--prod` without a draft check.
- Forgetting the publish dir: a build that succeeds but serves a 404.
- Relying on `_redirects` and `netlify.toml` redirects together without knowing which wins: use one.

## Review
- [ ] `netlify build` passes locally.
- [ ] Redirect order and fallbacks tested.
- [ ] No secrets in committed config.
- [ ] Long jobs use background functions or a queue.
- [ ] Security and cache headers set.
