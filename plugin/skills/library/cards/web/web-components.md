---
name: web-components
title: Web Components
area: web
tags: [web-components, custom-elements, shadow-dom, slots, events, a11y]
detect: []
related: [lit, htmx, playwright]
---
Native Web Components: custom elements, shadow DOM, slots and templates, with lifecycle, event and form traps.

## Verify
- `npx tsc --noEmit`: element classes and `HTMLElementTagNameMap` declarations type-check.
- `npx vitest run --browser.enabled`: runs tests in a real browser when Vitest browser mode is configured (jsdom lacks full custom-element and shadow support).
- `npx playwright test`: e2e interaction, focus and form behavior.
- `npx eslint .`: lint.

## Test first
Create the element, attach it, and assert through its shadow root and events.
```ts
import "./x-counter";

test("click increments and fires change", async () => {
  const el = document.createElement("x-counter") as HTMLElement & { count: number };
  document.body.append(el);
  const seen: number[] = [];
  el.addEventListener("change", e => seen.push((e as CustomEvent).detail));
  (el.shadowRoot!.querySelector("button") as HTMLButtonElement).click();
  expect(seen).toEqual([1]);
  el.remove();
});
```

## Do
- Name elements with a hyphen (`x-counter`) and register once: `if (!customElements.get("x-counter")) customElements.define(...)`.
- Build the DOM in `connectedCallback` (not the constructor), clean up listeners in `disconnectedCallback`.
- Declare `static observedAttributes` and handle `attributeChangedCallback`; keep attributes as strings and mirror to typed properties.
- Use `attachShadow({ mode: "open" })`, a `<template>` or adopted `CSSStyleSheet`, and `<slot>` for content projection.
- Communicate out with `new CustomEvent(name, { detail, bubbles: true, composed: true })` so events cross the shadow boundary.
- Theme with CSS custom properties and `::part()` rather than reaching inside.
- For form controls use `static formAssociated = true` and `attachInternals()`.
- Make them accessible: roles, labels, keyboard handling, and `delegatesFocus` where fitting.
- Declare the tag in `HTMLElementTagNameMap` for typed `createElement`.

## Avoid
- Reading attributes or children in the constructor: the element may not be parsed yet. Use `connectedCallback`.
- Adding listeners in `connectedCallback` without removing them: duplicates on re-attach. Remove in `disconnectedCallback`.
- Custom events without `composed: true` from inside shadow DOM: outside listeners never hear them.
- Assuming global CSS styles shadow content: it does not. Use custom properties, `::part` or adopted styles.
- Using `innerHTML` with untrusted strings: XSS. Use `textContent` or build nodes.
- Re-defining the same tag on hot reload: throws. Guard with `customElements.get`.
- Passing objects through attributes: they stringify to `[object Object]`. Use properties.

## Review
- [ ] Registration is guarded and the tag name has a hyphen.
- [ ] Listeners and observers are cleaned up on disconnect.
- [ ] Events are composed and typed, and properties reflect attributes.
- [ ] Styling hooks (variables and parts) are documented.
- [ ] Keyboard and screen reader behavior is tested in a real browser.
