---
name: markdown-rendering
title: Markdown rendering
area: domains
tags: [markdown, rendering, commonmark, xss, sanitize, links]
detect: [dep:marked, dep:markdown-it, dep:mistune]
related: [html-sanitization, rich-text-editors, unicode, docs]
---
Rendering user Markdown: a CommonMark parser, HTML disabled or sanitized after rendering, safe links, and stable heading anchors.

## Verify
- `pytest -q tests/test_markdown.py`: render and sanitization tests pass.
- `npx vitest run markdown`: JS render tests pass.
- `grep -rnE "dangerouslySetInnerHTML|innerHTML|\\|\\s*safe" src`: every raw-HTML sink should receive sanitized output.

## Test first
Markdown passes raw HTML and `javascript:` links through by default in many parsers.
```python
from app.md import render

def test_script_handlers_and_js_links_are_neutralized():
    html = render('hi <script>alert(1)</script> <img src=x onerror=alert(1)>\n\n'
                  '[a](javascript:alert(1)) [b](https://ok.example)')
    assert "<script" not in html and "onerror" not in html
    assert "javascript:" not in html
    assert 'href="https://ok.example"' in html
    assert 'rel="noopener' in html          # external links hardened
```

## Do
- Use a CommonMark-compliant parser (markdown-it, marked, mistune, cmark based) and pin its options in one module.
- Treat Markdown as untrusted input: disable raw HTML in the parser when you can; otherwise sanitize the HTML output with an allowlist sanitizer as the last step.
- Allow link schemes `http`, `https`, `mailto` only; add `rel="noopener noreferrer"` (and `nofollow` for user content) to external links.
- Generate heading ids by slugifying with a duplicate counter, so anchors stay unique and stable.
- Render on the server or at save time and cache; store the source Markdown, not only the HTML.
- Handle extensions deliberately: tables, task lists and footnotes via plugins; syntax highlighting after sanitization, using class names.
- Set `lang` hints and escape code block contents; test emoji and RTL text.
- Limit input size and nesting to avoid pathological slowdowns.

## Avoid
- `marked(userText)` straight into `innerHTML`: XSS. Sanitize, or use a renderer that escapes HTML.
- Sanitizing before rendering: Markdown can reintroduce markup. Sanitize the final HTML.
- Trusting autolinks: `javascript:` and `data:` schemes get through some configs. Allowlist schemes.
- Mixing two parsers (editor preview vs server): output differs. Share the module and options.
- Heading ids from raw text with no dedupe: collisions break anchors.
- Rendering on every request for large documents: precompute and cache.

## Review
- [ ] Raw HTML is disabled or sanitized after rendering.
- [ ] Link scheme allowlist and rel attributes present.
- [ ] One parser configuration is shared.
- [ ] Source Markdown is stored.
- [ ] XSS payload test exists.
