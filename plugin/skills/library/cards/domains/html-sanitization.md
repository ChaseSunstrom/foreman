---
name: html-sanitization
title: HTML sanitization
area: domains
tags: [xss, sanitize, html, dompurify, bleach, csp]
detect: [dep:dompurify, dep:bleach, dep:sanitize-html, dep:nh3]
related: [markdown-rendering, rich-text-editors, unicode, webhooks]
---
Making untrusted HTML safe: an allowlist sanitizer run once at the right place, with escaping as the default and CSP as a backstop.

## Verify
- `pytest -q tests/test_sanitize.py`: payload corpus tests pass.
- `npx vitest run sanitize`: JS side passes the same corpus.
- `grep -rnE "innerHTML|dangerouslySetInnerHTML|v-html|\\|\\s*safe|mark_safe" src`: every raw sink should be fed by the sanitizer.

## Test first
Run a hostile corpus and assert on the output, not the input.
```python
import pytest
from app.sanitize import clean

@pytest.mark.parametrize("bad", [
    '<img src=x onerror=alert(1)>',
    '<a href="javascript:alert(1)">x</a>',
    '<svg><script>alert(1)</script></svg>',
    '<p style="background:url(javascript:alert(1))">x</p>',
    '<scr<script>ipt>alert(1)</scr</script>ipt>',
])
def test_payloads_are_neutralized(bad):
    out = clean(bad).lower()
    assert "alert" not in out or "<" not in out.split("alert")[0].split(">")[-1]
    assert "onerror" not in out and "javascript:" not in out and "<script" not in out
```

## Do
- Prefer escaping (templating auto-escape) and text rendering; sanitize only where HTML is a real requirement.
- Use a maintained allowlist sanitizer: DOMPurify in browsers (or with jsdom on the server), nh3 or bleach in Python, sanitize-html in Node.
- Define the allowlist explicitly: tags, attributes per tag, URL schemes (`http`, `https`, `mailto`); drop `style`, event handlers, `iframe`, `object`, `form`.
- Sanitize on output (or at save time and store the clean result) and make that the last transformation before the sink.
- Add `rel="noopener noreferrer"` to links and consider `target` handling in an after-sanitize hook.
- Send a Content-Security-Policy with no `unsafe-inline` scripts as defense in depth.
- Keep the sanitizer version current; mutation-XSS fixes land regularly.
- Keep a payload corpus in tests and add every reported bypass.
- Use Trusted Types where supported to force sinks through a policy.

## Avoid
- Regex or string-replace stripping of `<script>`: trivially bypassed. Use a parser-based sanitizer.
- Denylist approaches: new vectors appear. Allowlist.
- Sanitizing then modifying the HTML (concatenation, replace): reopens holes. Sanitize last.
- Allowing `style` or `data:` URLs: CSS and script vectors. Drop or tightly allowlist.
- `bleach` or similar on whole pages with SVG and MathML allowed: namespace confusion. Keep those tags out.
- Sanitizing on input only, then rendering in another context (attribute, JS): context-specific escaping is still needed.

## Review
- [ ] All raw-HTML sinks are listed and sanitized.
- [ ] Allowlist is explicit and minimal.
- [ ] Sanitization is the final step.
- [ ] Payload corpus runs in CI.
- [ ] CSP is set.
