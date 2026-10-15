---
name: xss
title: Cross-site scripting
area: security
tags: [security, xss, html, csp, encoding, frontend]
detect: [dep:dompurify, dep:sanitize-html, dep:bleach, dep:nh3, dep:xss]
related: [security-headers, input-validation, csrf, sessions, cors]
---
XSS: encode on output for the exact context, sanitize any HTML you must allow, and back it with a strict CSP.

## Verify
- `semgrep scan --config p/xss --error`: no unsafe HTML sinks flagged.
- `grep -rnE "dangerouslySetInnerHTML|innerHTML\s*=|v-html|\|safe\b|mark_safe|html_safe|\{\{\{" src/`: every raw-HTML sink is listed and reviewed.
- `curl -sI localhost:3000 | grep -i content-security-policy`: a CSP header is present.

## Test first
Render a payload and assert it is inert.
```python
PAYLOADS = ['<script>alert(1)</script>', '"><img src=x onerror=alert(1)>', "javascript:alert(1)"]

import pytest
@pytest.mark.parametrize("p", PAYLOADS)
def test_comment_is_escaped(client, p):
    client.post("/comments", json={"body": p})
    html = client.get("/comments").text
    assert "<script>alert(1)</script>" not in html
    assert "<img src=x" not in html
```
For front ends, a component test with Testing Library that asserts `container.querySelector("script")` is null.

## Do
- Rely on the framework's auto-escaping (React JSX, Vue `{{ }}`, Jinja2 autoescape, Django templates, ERB `<%= %>`) and keep it on.
- Encode for the context: HTML body, attribute (quoted), URL, JavaScript, CSS each need their own encoder.
- When user HTML is required, sanitize with an allowlist library (DOMPurify, `bleach`/`nh3`, `sanitize-html`) at render time.
- Validate URL schemes (`http`, `https`, `mailto`) before putting user input in `href` or `src`.
- Set a CSP without `unsafe-inline`: `default-src 'self'`, nonces or hashes for scripts, `object-src 'none'`, `base-uri 'none'`.
- Use `textContent` over `innerHTML`, and set cookies `HttpOnly` so XSS cannot read sessions.
- Add `Content-Type: application/json` and `X-Content-Type-Options: nosniff` to API responses.

## Avoid
- `dangerouslySetInnerHTML`, `v-html`, `|safe`, `mark_safe`, `raw` on user data: they disable escaping. Sanitize first or render as text.
- Stripping `<script>` with regex: `<img onerror>`, SVG and event handlers pass. Use an allowlist sanitizer.
- Building HTML by string concatenation in JS (`el.innerHTML = "<b>" + name`): use DOM APIs or templates.
- `javascript:` URLs in `href` from user input: check the scheme.
- Putting user data inside `<script>` blocks via templating: use `JSON` data attributes or a JSON script tag with encoding.
- A CSP with `unsafe-inline` and `*`: it does not stop injection. Use nonces and an explicit source list.

## Review
- [ ] No raw-HTML sink receives unsanitized user data.
- [ ] URL attributes check the scheme.
- [ ] A strict CSP is set and reports are monitored.
- [ ] Session cookies are `HttpOnly`.
- [ ] A payload test covers each new place user text is rendered.
