---
name: cloudflare-pages
title: Cloudflare Pages
area: cloud
tags: [cloudflare, pages, static, functions, wrangler, deploy]
detect: [dep:wrangler, dep:@cloudflare/next-on-pages, file:wrangler.toml, file:wrangler.jsonc, file:_redirects, file:_headers]
related: [cloudflare-workers, cloudflare-d1-r2, netlify, vercel]
---
Cloudflare Pages: a build with a pinned Node version, preview per branch, Pages Functions for server logic, `_headers` and `_redirects` verified, secrets kept out of the repo.

## Verify
- `npx wrangler pages project list`: the project exists and is linked to the right account.
- `npx wrangler pages dev ./dist`: the built site and Functions run locally.
- `npx wrangler pages deployment list --project-name P`: recent deployments and their environments.
- `npx wrangler pages secret list --project-name P`: required secrets are set, with no values printed.
- `curl -sI https://BRANCH.P.pages.dev/`: the preview deploy serves with expected headers.

## Test first
Smoke test the built output for the routes, redirects and headers you depend on.
```js
test("security headers and SPA fallback", async () => {
  const r = await fetch(`${base}/deep/link`);
  expect(r.status).toBe(200);
  expect(r.headers.get("x-content-type-options")).toBe("nosniff");
});
```

## Do
- Pin the build: set the build command and output directory, `NODE_VERSION` as an environment variable (or a version file) so builds reproduce.
- Use Pages Functions in `functions/` (file-based routing) for server logic, and bindings (KV, D1, R2) declared in the wrangler config for that project.
- Set variables and secrets per environment (Production and Preview) so previews never touch production data.
- Define `_headers` for security headers (CSP, HSTS, `X-Content-Type-Options`) and long cache on hashed assets. Define `_redirects` for moves and SPA fallback (`/* /index.html 200`).
- Use the preview URL per branch for review, and protect previews with Cloudflare Access when they hold private content.
- Connect a custom domain and let Cloudflare issue the certificate.
- Commit the wrangler config so bindings and compatibility date are reviewable.
- Deploy from CI with a scoped API token (Pages edit only) when not using the Git integration.

## Avoid
- Committing `.dev.vars` or API tokens: put local secrets in an ignored `.dev.vars` and production ones through `wrangler pages secret put`.
- A global API key in CI: use a token limited to the account and Pages permission.
- Sharing one database or KV between Preview and Production bindings: previews can corrupt production. Bind separate resources.
- Unpinned Node versions: a platform default change breaks the build. Set `NODE_VERSION`.
- Node-only APIs in Functions without the compatibility flag: the Workers runtime is not Node. Set `compatibility_flags` such as `nodejs_compat` when needed, and check the dependency.
- Large uploads past the per-file size limit: host big assets in R2.
- Assuming redirects chain forever: rule counts are limited. Keep them lean.

## Review
- [ ] Build command, output directory and Node version are pinned.
- [ ] Preview and production have separate variables and bindings.
- [ ] `_headers` and `_redirects` are tested on a preview.
- [ ] No secrets in the repo, tokens scoped narrowly.
- [ ] Functions run under the Workers runtime constraints.
