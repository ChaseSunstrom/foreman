---
name: vercel
title: Vercel
area: cloud
tags: [vercel, deploy, serverless, edge, nextjs, env]
detect: [dep:vercel, dep:@vercel/node, dep:@vercel/analytics, dep:@vercel/blob, dep:@vercel/kv, dep:@vercel/postgres, file:vercel.json, file:.vercel/project.json]
related: [netlify, cloudflare-workers, cloud-cost]
---
Vercel deployments: preview and production builds, `vercel.json` routing, environment variables per scope, function limits.

## Verify
- `npx vercel build`: the production build runs locally with project settings (needs `vercel pull` first).
- `npx vercel env ls`: variables exist per environment (production, preview, development).
- `npx vercel deploy`: creates a preview deployment and prints its URL.
- `npx vercel logs DEPLOYMENT_URL`: runtime logs for a deployment.
- `curl -fsS https://PREVIEW_URL/api/health`: the preview works before promotion.

## Test first
Run a smoke check against the preview URL; unit tests stay in the framework.
```typescript
import { test, expect } from "vitest";

test("preview health endpoint is up", async () => {
  const res = await fetch(`${process.env.PREVIEW_URL}/api/health`);
  expect(res.status).toBe(200);
});
```
Add a routing test for any `rewrites`, `redirects` or `headers` you add to `vercel.json`.

## Do
- Keep project settings (framework, build command, output) in `vercel.json` or the dashboard, not both.
- Set environment variables per scope with `vercel env add NAME production`; use `vercel env pull .env.local` for dev.
- Prefix browser-exposed values as the framework requires (`NEXT_PUBLIC_`); everything else stays server-side.
- Set function `maxDuration` and `regions` in `vercel.json` or route config; put functions near the database.
- Add `Cache-Control` and `s-maxage` or `stale-while-revalidate` for cacheable API responses.
- Use preview deployments for review; protect them with Deployment Protection.
- Use cron through the `crons` key in `vercel.json` and secure the route with `CRON_SECRET`.
- Choose edge runtime only for code that uses web APIs alone.

## Avoid
- Committing `.vercel/` or `.env*.local`: add them to `.gitignore`.
- Secrets in `NEXT_PUBLIC_*` or client bundles: they ship to browsers.
- Writing to the filesystem at runtime: it is read-only except `/tmp`, and ephemeral.
- Long-running work in a function: it hits the duration limit. Use a queue or background service.
- `vercel --prod` from a laptop as the release path: use Git-based deploys and promote a verified preview.
- Changing an env var and expecting a live update: redeploy.
- Connecting serverless functions to Postgres without pooling.

## Review
- [ ] Env vars are scoped and none are secret in public prefixes.
- [ ] `vercel.json` routes tested; no duplicate settings in the dashboard.
- [ ] Function duration and region set.
- [ ] Preview was checked before promotion.
- [ ] Cron routes require the secret.
