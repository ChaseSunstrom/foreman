---
name: web-scraping
title: Web Scraping
area: domains
tags: [scraping, crawling, parsing, playwright, robots-txt, rate-limiting]
detect: [dep:beautifulsoup4, dep:scrapy, dep:cheerio, dep:puppeteer, dep:selectolax, dep:lxml, dep:colly, dep:crawlee, dep:parsel, dep:goquery]
related: [unicode, cron-jobs, search, legacy-code]
---
Polite, resilient data extraction: prefer APIs, parse with selectors, throttle, cache, and treat the output as untrusted.

## Verify
- `curl -s https://example.com/robots.txt`: crawl rules and delays to honor.
- `curl -sI https://example.com/page`: status, `ETag`, `Last-Modified` for conditional requests.
- `pytest -q tests/test_parsers.py`: parsers pass against saved HTML fixtures with no network.
- `python -c "import json,sys; [json.loads(l) for l in open('out.jsonl')]"`: output is valid JSON Lines.

## Test first
Save real pages as fixtures; test the parser offline, including the broken variant.
```python
from pathlib import Path
from app.parse import parse_product

def test_parses_price_and_title():
    html = Path("tests/fixtures/product.html").read_text(encoding="utf-8")
    p = parse_product(html)
    assert p == {"title": "Widget", "price_minor": 1999, "currency": "USD"}

def test_layout_change_raises_not_returns_garbage():
    import pytest
    with pytest.raises(ValueError):
        parse_product("<html><body>redesigned</body></html>")
```

## Do
- Look first for an official API, a sitemap, an RSS feed or embedded JSON (`script[type="application/ld+json"]`, `__NEXT_DATA__`, XHR endpoints in the network tab).
- Respect `robots.txt`, terms of service and copyright; identify with a descriptive `User-Agent` and contact.
- Throttle per host (1 to 2 requests per second or less), add jitter, and back off on 429 and 5xx using `Retry-After`.
- Cache responses on disk and send `If-None-Match` or `If-Modified-Since`; make the crawl resumable with a persistent frontier.
- Use CSS selectors or XPath on a real parser (`lxml`, `selectolax`, `cheerio`); anchor on stable attributes, not position.
- Use a headless browser (Playwright) only when content needs JavaScript; wait for a specific selector, not a fixed sleep.
- Validate each record against a schema; log and count parse failures; alert when the failure rate jumps.
- Normalize text (strip, collapse whitespace, NFC) and resolve relative URLs with `urljoin`.
- Deduplicate by canonical URL or content hash.

## Avoid
- Regex over HTML: breaks on nesting and attributes. Use a parser.
- Fixed `sleep()` waits in browsers: flaky and slow. Wait for conditions.
- Hammering a host with unbounded concurrency: bans and harm to the site. Cap per-domain concurrency.
- Putting scraped HTML into your pages unsanitized: stored XSS. Escape or sanitize.
- Following links blindly: crawler traps and infinite calendars. Set depth, URL pattern and page limits.
- Hardcoding deep `div > div:nth-child(3)` selectors: break on trivial redesigns. Use semantic hooks.
- Ignoring encoding: mojibake. Decode using response headers and meta, defaulting to UTF-8.
- Bypassing logins, paywalls or CAPTCHAs: legal and ethical risk. Get permission or a data license.
- Storing personal data without a basis: see the gdpr card.

## Review
- [ ] Parsers have fixtures and fail loudly on layout changes.
- [ ] Rate limits, backoff, caching and a clear User-Agent are in place.
- [ ] Robots and terms were checked and the decision recorded.
- [ ] Output is schema-validated, deduplicated and sanitized.
- [ ] Crawl is resumable, bounded and monitored.
