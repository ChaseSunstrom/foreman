---
name: vue-composition-api
title: Vue Composition API
area: web
tags: [vue, composition-api, script-setup, reactivity, composables, typescript]
detect: [dep:vue, dep:vue-tsc, dep:@vue/test-utils]
related: [vue, pinia, nuxt]
---
Vue 3 Composition API: script setup, refs and reactive state, computed, watchers and composables with typed props and emits.

## Verify
- `npx vue-tsc --noEmit`: template and script types, including props and emits.
- `npx vitest run`: component and composable tests.
- `npx eslint .`: with `eslint-plugin-vue` it catches reactivity-loss and prop-mutation patterns.
- `npm run build`: production build.

## Test first
Mount with `@vue/test-utils` and assert on rendered output and emitted events.
```ts
import { mount } from "@vue/test-utils";
import Counter from "./Counter.vue";

test("emits update on click", async () => {
  const w = mount(Counter, { props: { modelValue: 1 } });
  await w.get("button").trigger("click");
  expect(w.emitted("update:modelValue")![0]).toEqual([2]);
});
```

## Do
- Use `<script setup lang="ts">` with `defineProps<{...}>()`, `defineEmits<{...}>()` and `defineModel()` where the installed version supports it.
- Use `ref` for primitives and replaceable objects; `computed` for derived values (cached, no side effects).
- Use `watch` for side effects on specific sources; `watchEffect` only for simple auto-tracked cases; clean up with the callback's `onCleanup`.
- Extract reusable logic into `useX()` composables that return refs and functions, accept `MaybeRefOrGetter` inputs and read them with `toValue`.
- Destructure reactive objects with `toRefs` or `toRef`, or pass getters.
- Use `storeToRefs` when destructuring a Pinia store.
- Register lifecycle hooks (`onMounted`, `onUnmounted`) synchronously in `setup`.

## Avoid
- Destructuring a `reactive` object or props into plain variables: reactivity is lost. Use `toRefs` or access via the object.
- Mutating props: Vue warns and parent state drifts. Emit an event or use `defineModel`.
- Forgetting `.value` in script (not in templates): the ref object is used instead of its value.
- Side effects inside `computed`: they run unpredictably. Use `watch`.
- Registering `onMounted` after an `await` in `setup`: the hook is not attached. Register before awaiting.
- Options API `this` habits (`this.$refs`, `mixins`): use template refs (`ref="el"` with `const el = ref(null)`) and composables.
- Deep `watch` on large objects by default: it is costly. Watch the specific field.

## Review
- [ ] Props and emits are fully typed and `vue-tsc` is clean.
- [ ] No reactive destructuring that drops reactivity.
- [ ] Watchers and listeners are cleaned up on unmount.
- [ ] Composables take refs or getters and are tested alone.
- [ ] No prop mutation and no side effects in `computed`.
