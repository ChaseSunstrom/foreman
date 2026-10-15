---
name: nextjs-app-router
title: Next.js App Router
area: web
tags: [nextjs, app-router, routing, layouts, server-actions, metadata]
detect: [file:*app/layout.tsx, file:*app/layout.jsx, file:*app/layout.js]
related: [nextjs, react-server-components, nextjs-caching, nextjs-middleware, react-suspense]
---
Next.js App Router: file-convention routes, nested layouts, route handlers, server actions and the metadata API.

## Verify
- `npx tsc --noEmit`: route params, props and action types check.
- `npx next build`: static and dynamic rendering errors surface, and the route table shows which pages are static.
- `npx eslint .`: lint rules.
- `npx playwright test`: end-to-end navigation and form flows.

## Test first
Unit-test route handlers by calling the exported function with a `Request`.
```ts
// app/api/items/route.test.ts
import { POST } from "./route";

test("POST rejects an empty name", async () => {
  const res = await POST(new Request("http://t/api/items", {
    method: "POST", body: JSON.stringify({ name: "" }),
  }));
  expect(res.status).toBe(400);
});
```

## Do
- Use the file conventions: `page`, `layout`, `loading`, `error`, `not-found`, `route`. `error.tsx` must be a client component.
- Keep shared UI in `layout.tsx`; it does not re-render on navigation, so do not read per-page state there.
- Validate server action input with a schema (zod or similar) and check the session inside every action: actions are public POST endpoints.
- Use `generateMetadata` for dynamic titles; `generateStaticParams` for known dynamic segments.
- Use `<Link>` for navigation, `redirect()` and `notFound()` from `next/navigation`, `revalidatePath` or `revalidateTag` after a mutation.
- Group with `(group)` folders and scope with `[slug]`, `[...rest]`, `@slot` as needed.
- Use `next/image` and `next/font` for assets.

## Avoid
- Treating `params` and `searchParams` as plain objects in recent versions: they are promises in newer releases, so `await` them or check the installed version's types.
- Mixing `pages/` and `app/` routes for the same path: the build errors. Migrate one path at a time.
- Calling `redirect()` inside `try/catch`: it throws a control-flow error that gets swallowed. Call it outside or rethrow.
- Fetching your own route handler from a server component: call the shared function directly.
- Reading `cookies()` or `headers()` in a page you expect to be static: it opts the route into dynamic rendering.
- Trusting client-sent ids in server actions without an ownership check.

## Review
- [ ] Each action and route handler authenticates, authorizes and validates input.
- [ ] `"use client"` appears only where needed, and `loading.tsx` or `Suspense` covers slow segments.
- [ ] The build output shows the expected static or dynamic mode per route.
- [ ] Mutations revalidate the paths or tags that show the changed data.
- [ ] Metadata, `not-found` and `error` states exist for dynamic routes.
