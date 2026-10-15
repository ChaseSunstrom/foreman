---
name: vue
title: Vue
area: web
tags: [vue, javascript, typescript, ui, composition-api, sfc]
detect: [dep:vue, ext:.vue]
related: [pinia, nuxt, vitest, testing-library, playwright, tailwind]
---
Vue 3 single-file components with `<script setup>`, the Composition API and reactive refs.

## Verify
- `npx vue-tsc --noEmit`: template and script types.
- `npx eslint . --max-warnings 0`: with `eslint-plugin-vue`.
- `npx vitest run`: component tests with `@vue/test-utils`.
- `npm run build`: production build.

## Test first
Mount components with `@vue/test-utils` in `*.spec.ts` and assert on rendered output after `await`.
```ts
import { mount } from "@vue/test-utils";
import { expect, test } from "vitest";
import Counter from "./Counter.vue";

test("increments", async () => {
  const w = mount(Counter);
  await w.get("button").trigger("click");
  expect(w.text()).toContain("1");
});
```

## Do
- Use `<script setup lang="ts">` with `defineProps<{...}>()` and `defineEmits<{...}>()`.
- Use `ref` for primitives and `reactive` sparingly; access refs with `.value` in script only.
- Derive values with `computed`; use `watch` only for side effects.
- Give every `v-for` a `:key` with a stable id; never combine `v-for` and `v-if` on one element.
- Pass data down by props and up by emits; use `provide`/`inject` for subtree-wide values.
- Extract reusable stateful logic into composables (`useX()` returning refs).
- Clean up in `onUnmounted` (listeners, timers) or use `watchEffect` with `onWatcherCleanup`/cleanup callback.

## Avoid
- Options API and `Vue.extend` in new code, or `this`-based mixins: use composables.
- Destructuring a `reactive` object or props (`const { x } = props`) and expecting reactivity: it is lost. Use `toRefs`, `toRef` or access `props.x`.
- Mutating a prop: Vue warns and parent state diverges. Emit an event or use `defineModel`.
- `v-html` with user input: XSS. Render as text or sanitize.
- Losing reactivity by replacing a `reactive` root (`state = {...}`): assign into it or use a `ref`.
- `watch` with a getter missing: `watch(obj.prop, ...)` watches a value, not the property. Use `watch(() => obj.prop, ...)`.
- Vue 2 APIs (`$on`, `$listeners`, filters, `new Vue`): removed in 3.

## Review
- [ ] Props and emits are typed, and no prop is mutated.
- [ ] No `v-for` without a stable `:key`.
- [ ] Reactivity survives every destructure (`toRefs`) and every reassign.
- [ ] Watchers and listeners clean up on unmount.
- [ ] Tests use `await nextTick()` or awaited `trigger` before asserting.
