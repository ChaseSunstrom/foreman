---
name: email-design
title: Email Design
area: ux
tags: [ux, email, html-email, mjml, tables, dark-mode, deliverability]
detect: [dep:mjml, dep:react-email, dep:@react-email/components, dep:maizzle]
related: [dark-mode, accessibility, calls-to-action, color-contrast, image-optimization, brand-identity]
---
HTML email is 600 px, table-based, inline-styled, image-light and readable with images off and in dark mode.

## Verify
- `npx mjml email.mjml -o dist/email.html --config.validationLevel=strict`: compiles table markup and flags invalid structure.
- `wc -c dist/email.html`: under 102 KB (Gmail clips beyond that).
- `grep -cE "display: *(flex|grid)|position: *(absolute|fixed)" dist/email.html`: should be 0.
- Send to a Litmus, Email on Acid or Mailtrap preview; check Outlook (Word renderer), Gmail and Apple Mail, light and dark.
- `grep -c "<img" dist/email.html` against `grep -c 'alt=' dist/email.html`: every image has alt.

## Test first
```python
import re, pathlib

def test_email_constraints():
    html = pathlib.Path("dist/email.html").read_text()
    assert len(html.encode()) < 102_000, "Gmail clips over 102 KB"
    assert not re.search(r"display:\s*(flex|grid)|position:\s*(absolute|fixed)", html)
    assert re.search(r'width="600"|max-width:\s*600px', html)
    imgs = re.findall(r"<img\b[^>]*>", html)
    assert all("alt=" in i and "width=" in i for i in imgs)
    assert re.search(r'role="presentation"', html), "layout tables need role=presentation"
```

## Do
- Layout: a centered 600 px wide table (`max-width: 600px`, fluid below), one column on mobile via media query, `role="presentation"` on layout tables.
- Inline all CSS (the build tool does this); keep a `<style>` for media queries and dark mode only.
- Font stack with web-safe fallback (`Arial, Helvetica, sans-serif`), body 16 px, line-height 1.5, preheader text 40-100 characters.
- Buttons are bulletproof: a table cell with background color and padded `<a>`, 44 px high, not an image.
- Images: set `width`, `height`, `alt`, `display:block`; host on HTTPS; provide 2x for retina; the message must work with images blocked.
- Dark mode: `<meta name="color-scheme" content="light dark">` plus `@media (prefers-color-scheme: dark)`, transparent PNG logos with a light outline, avoid pure white images.
- Include a plain-text part, an unsubscribe link and the physical address (legal); `List-Unsubscribe` header.
- Subject under 50 characters; one CTA; links with full URLs and UTM tags.
- Sender authentication: SPF, DKIM and DMARC passing.

## Avoid
- Flexbox, grid, JS, forms, web fonts as essentials, background images as the only content.
- One large image as the whole email: blocked images means a blank email, and spam filters dislike it.
- Low-contrast gray text; Outlook ignores many margins and `max-width` (use ghost tables).
- Tracking pixels without consent where laws require it.

## Review
- [ ] Renders in Outlook, Gmail and Apple Mail, light and dark, with images off.
- [ ] Under 102 KB, 600 px, tables only, with alt text on every image.
- [ ] Has a plain-text part, unsubscribe, SPF/DKIM/DMARC pass.
- [ ] A single clear CTA that is a real link, not an image.
