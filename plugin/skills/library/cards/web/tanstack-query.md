---
name: tanstack-query
title: TanStack Query
area: web
tags: [tanstack-query, react-query, data-fetching, cache, async, react]
detect: [dep:@tanstack/react-query, dep:@tanstack/vue-query, dep:@tanstack/svelte-query, dep:@tanstack/solid-query, dep:@tanstack/angular-query-experimental]
related: [react, msw, testing-library, redux-toolkit, zustand]
---
TanStack Query: server state as cached queries and mutations keyed by query keys.

## Verify
- `npx tsc --noEmit`: typed query data and keys.
- `npx eslint . --max-warnings 0`: with `@tanstack/eslint-plugin-query` (exhaustive query-key deps, stable client).
- `npx vitest run`: hooks tested through a provider with a fresh client.

## Test first
Give each test its own `QueryClient` with `retry: false`, and mock the network with MSW.
```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { useUser } from "./useUser";

test("loads the user", async () => {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const wrapper = ({ children }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>;
  const { result } = renderHook(() => useUser(7), { wrapper });
  await waitFor(() => expect(result.current.isSuccess).toBe(true));
  expect(result.current.data?.name).toBe("Ada");
});
```

## Do
- Use the object form: `useQuery({ queryKey: ["user", id], queryFn: ... })`.
- Put every input the function uses in the `queryKey`; build keys with a small factory.
- Create the `QueryClient` once (module scope or `useState`), outside render.
- Mutate with `useMutation` and in `onSuccess` call `queryClient.invalidateQueries({ queryKey })`.
- Throw on non-2xx inside `queryFn` (`fetch` does not reject on 404).
- Set `staleTime` deliberately; the default of 0 refetches on every mount and focus.
- Use `enabled` for dependent queries and `select` to derive a slice.
- For optimistic updates, snapshot in `onMutate`, roll back in `onError`, invalidate in `onSettled`.

## Avoid
- The v3 positional signature `useQuery(key, fn)` and `isLoading` semantics from old docs: v5 uses a single object and `isPending`. Check the installed version.
- `new QueryClient()` inside a component body: the cache resets every render. Memoize it.
- Copying query data into `useState`: it goes stale. Use `data` directly or `select`.
- Missing variables in `queryKey`: wrong cached data shown across inputs. Include them all.
- A `queryFn` that returns `undefined`: not allowed, so return `null` or data.
- Retries left on in tests: slow failures and timeouts. Set `retry: false`.
- Sharing one `QueryClient` across SSR requests: leaks data between users. Create per request.

## Review
- [ ] Every query key contains all variables the fetcher reads.
- [ ] Mutations invalidate or update the affected keys.
- [ ] Errors surface (error state UI or error boundary), and non-OK responses throw.
- [ ] `staleTime` and `gcTime` are chosen, not left to chance.
- [ ] Tests use a fresh client per test with retries off.

## Notes
Package names differ per framework adapter; the detect list covers the common ones.
