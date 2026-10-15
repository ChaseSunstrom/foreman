---
name: pinia
title: Pinia
area: web
tags: [vue, pinia, state, store, typescript]
detect: [dep:pinia]
related: [vue, nuxt, vitest]
---
Pinia stores for Vue: setup or options stores with state, getters and actions, tested with a fresh active Pinia.

## Verify
- `npx vue-tsc --noEmit`: store and getter types.
- `npx vitest run`: store and component tests.
- `npx eslint . --max-warnings 0`: lint.

## Test first
Create a fresh Pinia per test; test actions and getters directly, no component needed.
```ts
import { beforeEach, expect, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useCartStore } from "./cart";

beforeEach(() => setActivePinia(createPinia()));

test("adding an item updates the total", () => {
  const cart = useCartStore();
  cart.add({ id: 1, price: 5 });
  expect(cart.total).toBe(5);
});
```
For components, use `createTestingPinia` from `@pinia/testing` (actions are stubbed unless `stubActions: false`).

## Do
- Define stores with `defineStore("id", ...)`, one per domain, with unique ids.
- Prefer setup stores (`defineStore("x", () => { const n = ref(0); return { n } })`) and return every state ref, getter and action.
- Put derived values in getters (`computed`) and all mutations in actions.
- Destructure state and getters with `storeToRefs(store)`; destructure actions directly.
- Call `useXStore()` inside `setup`, actions or after `app.use(createPinia())`, not at module top level.
- Reset with `$reset()` (options stores) or write your own reset action for setup stores.
- Call `await` in actions and handle errors there; keep components thin.

## Avoid
- Destructuring state straight off the store (`const { count } = store`): reactivity lost. Use `storeToRefs`.
- Vuex idioms (`mutations`, `commit`, `dispatch`, `mapState`): Pinia has none. Call actions directly.
- Calling `useStore()` before Pinia is installed (module scope, router guards at import time): "getActivePinia" error. Call it inside the function.
- A setup store that does not return a ref: it is not state, not SSR-serialized and not devtools-visible. Return everything.
- Sharing one Pinia between tests: leaked state. Create one in `beforeEach`.
- Storing non-serializable values (class instances, DOM nodes) in state under SSR: hydration breaks. Keep plain data.
- `store.$state = {...}` replacing wholesale: use `$patch` for batched updates.

## Review
- [ ] Mutations happen only in actions; getters are pure.
- [ ] Components use `storeToRefs` for reactive reads.
- [ ] Setup stores return all state, getters and actions.
- [ ] Each test activates its own Pinia.
- [ ] Persisted or SSR state is plain, serializable data.
