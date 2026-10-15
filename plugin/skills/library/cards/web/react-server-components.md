---
name: react-server-components
title: React Server Components
area: web
tags: [react, rsc, server, client, serialization, streaming]
detect: [dep:react-server-dom-webpack, dep:react-server-dom-turbopack, dep:react-server-dom-parcel]
related: [nextjs-app-router, react-suspense, nextjs-caching, react]
---
React Server Components: server-only render tree, a strict client boundary, and props that must serialize.

## Verify
- `npx tsc --noEmit`: props crossing the boundary type-check.
- `npx eslint .`: hooks rules and import restrictions still hold.
- `npm run build`: the bundler rejects server-only code pulled into a client module.
- `npx vitest run`: pure logic and client components pass (async server components are not rendered by jsdom).

## Test first
Server components are async functions: test the data layer and the client leaf separately, and cover the page with one e2e test.
```tsx
// components/Counter.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

test("increments on click", async () => {
  render(<Counter initial={2} />);
  await userEvent.click(screen.getByRole("button", { name: /add/i }));
  expect(screen.getByText("3")).toBeInTheDocument();
});
```

## Do
- Default to server components. Add `"use client"` only to the smallest leaf that needs state, effects, refs or browser APIs.
- Fetch data with `await` directly in the server component; run independent fetches with `Promise.all` to avoid waterfalls.
- Pass server components to client components as `children` or props: a client file can render a server tree it did not import.
- Mark server-only modules with `import "server-only"` so secrets and DB clients cannot reach the client bundle.
- Pass only serializable props: primitives, plain objects, arrays, Date, Map, Set, promises, server actions.
- Wrap slow subtrees in `<Suspense>` so the shell streams first.
- Dedupe per-request reads with `React.cache`.

## Avoid
- `"use client"` at the layout or page root: the whole subtree ships as JS. Push it down to leaves.
- Passing functions, class instances or event handlers from server to client props: serialization fails. Use a server action or define the handler in the client file.
- `useState`, `useEffect`, `useContext` or `onClick` in a server component: build error. Extract a client child.
- Putting `process.env.SECRET` reads in shared files: they leak when a client file imports them. Keep them behind `server-only`.
- Creating context providers in a server component: providers must be client components that take `children`.
- Sequential `await` of independent fetches: parallelize with `Promise.all`.

## Review
- [ ] Every `"use client"` file needs interactivity and sits as deep as possible.
- [ ] No secret, DB client or ORM import is reachable from a client module.
- [ ] Props across the boundary are serializable and small, with no whole DB rows with private fields.
- [ ] Independent fetches are parallel and slow ones sit under `Suspense`.
- [ ] Mutations go through server actions that validate input and check auth.
