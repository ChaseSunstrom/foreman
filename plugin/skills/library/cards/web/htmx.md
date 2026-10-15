---
name: htmx
title: htmx
area: web
tags: [htmx, hypermedia, html, server-rendered, ajax, partials]
detect: [dep:htmx.org, dep:django-htmx]
related: [alpine, tailwind, playwright, fastapi]
---
htmx: server returns HTML fragments, `hx-*` attributes swap them into the page; the server owns state and rendering.

## Verify
- `curl -s -H "HX-Request: true" localhost:8000/items | head`: the endpoint returns a fragment, not a full page.
- `curl -si localhost:8000/items | head -20`: the same URL without the header returns a full page (if you support both).
- `npx playwright test`: user-level flows including swaps and focus.

## Test first
Test the endpoint as HTML first: assert the partial has the markup and the right status, then the full flow in a browser.
```python
def test_add_item_returns_row_fragment(client):
    r = client.post("/items", data={"name": "milk"}, headers={"HX-Request": "true"})
    assert r.status_code == 200
    assert "<tr" in r.text and "milk" in r.text
    assert "<html" not in r.text
```
Use your stack's harness; the shape stays: send `HX-Request`, assert fragment.

## Do
- Return HTML partials from endpoints and reuse the same template for the full page and the fragment.
- Set `hx-target` and `hx-swap` explicitly (`outerHTML`, `beforeend`, `innerHTML`); default is `innerHTML` of the triggering element.
- Return 4xx with an error fragment and opt in to swapping it in an `htmx:beforeSwap` handler (`evt.detail.shouldSwap = true`); htmx does not swap 4xx/5xx by default.
- Use `hx-boost="true"` on a container to upgrade normal links and forms.
- Send CSRF tokens on mutating requests: `hx-headers='{"X-CSRFToken": "..."}'` or on `<body>`.
- Use `HX-Redirect`, `HX-Trigger` and `HX-Retarget` response headers for server-driven control.
- Add `hx-indicator` and disable inputs during requests; use `hx-sync` to stop racing requests.
- Escape all interpolated values in templates (autoescape on).

## Avoid
- Returning JSON and rendering it client-side: that is a SPA. Return HTML.
- Assuming error responses swap: they do not, so users see nothing. Handle `htmx:responseError` or configure swapping 422.
- Skipping CSRF because "it is AJAX": cookies are still sent. Send the token.
- `hx-swap-oob` everywhere: hidden coupling. Prefer a single target, and OOB only for out-of-band bits like counters.
- Loading htmx from a third-party CDN without a pinned version or SRI hash: supply-chain risk. Vendor or pin it.
- Inline user content in `hx-vals` or `hx-on` attributes unescaped: XSS. Escape or use data endpoints.
- Putting the interactive state in the DOM only and re-swapping it: loses focus and input. Use `hx-preserve` or swap smaller regions.

## Review
- [ ] Every endpoint returns a fragment for `HX-Request` and handles direct navigation sensibly.
- [ ] Errors are visible to the user (swap config or error handler).
- [ ] Mutating requests carry CSRF tokens.
- [ ] Targets and swap modes are explicit and focus is preserved where needed.
- [ ] Templates autoescape all dynamic content.
