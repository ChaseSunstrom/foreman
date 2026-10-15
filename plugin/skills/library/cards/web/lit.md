---
name: lit
title: Lit
area: web
tags: [lit, web-components, custom-elements, shadow-dom, typescript]
detect: [dep:lit, dep:lit-element]
related: [storybook, playwright, typescript, vitest]
---
Lit web components: `LitElement` classes with reactive properties, tagged `html` templates, scoped `css`.

## Verify
- `npx tsc --noEmit`: decorator and property types (needs `experimentalDecorators` or the standard decorators setup matching your Lit version).
- `npx web-test-runner "src/**/*.test.ts" --node-resolve`: tests in a real browser.
- `npx eslint . --max-warnings 0`: with `eslint-plugin-lit`.
- `npm run build`: bundle or `tsc` output.

## Test first
Test in a real browser with `@open-wc/testing`: fixture, await `updateComplete`, assert on shadow DOM.
```ts
import { fixture, html, expect } from "@open-wc/testing";
import "./my-counter.js";

it("increments", async () => {
  const el = await fixture(html`<my-counter></my-counter>`);
  el.shadowRoot!.querySelector("button")!.click();
  await (el as any).updateComplete;
  expect(el.shadowRoot!.textContent).to.contain("1");
});
```

## Do
- Define elements with `@customElement("my-x")` or `customElements.define`; names need a hyphen.
- Declare reactive state with `@property()` for public attributes and `@state()` for private internal state.
- Style in `static styles = css\`...\``; style from outside through CSS custom properties and `::part()`.
- Render with `render() { return html\`...\`; }`; bind with `.prop=${}`, `?bool=${}`, `@event=${}`.
- Communicate upward with `this.dispatchEvent(new CustomEvent("x", { detail, bubbles: true, composed: true }))`.
- Await `this.updateComplete` after state changes when reading the DOM.
- Use `repeat(items, i => i.id, ...)` for keyed lists that reorder.
- Clean up listeners in `disconnectedCallback`, calling `super`.

## Avoid
- `innerHTML` or `unsafeHTML` with user content: XSS. Bind text through templates.
- Mutating arrays or objects in a `@property` in place: no update. Assign a new reference or call `requestUpdate()`.
- Setting properties in `updated()` without a guard: extra render loops. Use `willUpdate` for derived values.
- Forgetting `super.connectedCallback()` or `super.disconnectedCallback()`: breaks Lit's controllers.
- Querying `document` for elements inside the component: they are in shadow DOM. Use `this.renderRoot.querySelector` or `@query`.
- Class field shadowing property accessors (`useDefineForClassFields` true with decorators): properties stop being reactive. Set it false, or use the `accessor` keyword with standard decorators.
- Attribute names with camelCase: HTML lowercases them. Set `attribute: "my-attr"` or use property binding.

## Review
- [ ] Public API is `@property` with a type and default; internals are `@state`.
- [ ] Events cross shadow boundaries only where intended (`composed`).
- [ ] No in-place mutation of reactive data.
- [ ] Listeners and observers are removed on disconnect.
- [ ] Tests run in a real browser and await `updateComplete`.
