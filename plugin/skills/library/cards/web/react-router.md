---
name: react-router
title: React Router
area: web
tags: [react, router, routing, loaders, actions, spa]
detect: [dep:react-router, dep:react-router-dom]
related: [react, testing-library, playwright, tanstack-query, msw]
---
React Router: route objects with loaders and actions, nested layouts with `Outlet`, navigation by links and forms.

## Verify
- `npx tsc --noEmit`: route params and loader data types compile.
- `npx vitest run`: route tests pass through an in-memory router.
- `npm run build`: bundle builds; framework mode also generates route types.
- `npx eslint . --max-warnings 0`: hooks and imports are clean.

## Test first
Render routes with `createMemoryRouter` and assert on what the user sees after the loader resolves.
```tsx
import { createMemoryRouter, RouterProvider } from "react-router-dom";
import { render, screen } from "@testing-library/react";
import { routes } from "./routes";

test("shows the user from the loader", async () => {
  const router = createMemoryRouter(routes, { initialEntries: ["/users/7"] });
  render(<RouterProvider router={router} />);
  expect(await screen.findByRole("heading", { name: "Ada" })).toBeInTheDocument();
});
```
Mock the network (MSW) rather than the loader.

## Do
- Define routes as data (`createBrowserRouter`) and nest them so layouts render an `<Outlet />`.
- Load data in route `loader`s and read it with `useLoaderData`; mutate in `action`s via `<Form>`.
- Return `redirect("/login")` from loaders and actions for auth failures.
- Throw `Response`s or errors and render them in a route `errorElement`.
- Use `<Link>` and `<NavLink>` for navigation, `useNavigate` only for imperative flows after an event.
- Read query string with `useSearchParams`; keep filter state in the URL.
- Check the installed version's import path: current majors export from `react-router`, older ones from `react-router-dom`.

## Avoid
- Fetching in `useEffect` inside route components: waterfalls and flashes of empty UI. Use a `loader`.
- Switch-era APIs (`<Switch>`, `component=`, `useHistory`, `<Redirect>`): removed. Use `<Routes>`/route objects, `element`, `useNavigate`, `<Navigate>`.
- `window.location.href = ...` for in-app moves: full reload loses state. Use `navigate` or `<Link>`.
- Absolute child paths under a parent (`path="/child"` nested): breaks nesting. Use relative paths.
- Auth checks only in components: the loader still runs and fetches. Guard in the loader.
- Ignoring `navigation.state`: double submits. Disable the button while `submitting`.

## Review
- [ ] Every data route has an `errorElement` or inherits one.
- [ ] Auth redirects happen in loaders and actions, not after render.
- [ ] Mutations use `action` and `<Form>` (or `useFetcher`) and revalidate the loader data.
- [ ] Links are real anchors; no `onClick` navigation on non-links.
- [ ] Tests render through a memory router with the real route table.
