---
name: rss-feeds
title: RSS and Atom feeds
area: domains
tags: [rss, atom, feeds, polling, caching, xml]
detect: [dep:feedparser, dep:rss-parser, dep:feed]
related: [web-scraping, cron-jobs, html-sanitization, webhooks]
---
Publishing and consuming feeds: valid RSS or Atom, stable GUIDs, conditional GET, polite polling, and sanitized item HTML.

## Verify
- `xmllint --noout feed.xml`: the feed is well-formed XML.
- `pytest -q tests/test_feeds.py`: generation, parsing and dedupe tests pass.
- `curl -sI -H 'If-None-Match: "etag"' http://localhost:8000/feed.xml`: the endpoint answers 304 for a matching ETag.

## Test first
Item identity must survive edits and republishing.
```python
from app.feeds import ingest, build_rss

def test_guid_dedupes_and_dates_are_rfc822(db):
    item = {"guid": "post-42", "title": "A", "link": "https://x.test/a", "updated": "2026-03-08T01:30:00Z"}
    ingest(db, [item]); ingest(db, [{**item, "title": "A (edited)"}])
    assert db.count_items() == 1 and db.item("post-42").title == "A (edited)"
    xml = build_rss(db.items())
    assert "<pubDate>Sun, 08 Mar 2026 01:30:00 +0000</pubDate>" in xml
    assert '<guid isPermaLink="false">post-42</guid>' in xml
```

## Do
- Emit valid feeds: RSS 2.0 or Atom, with channel title, link, description, and per item a unique `guid` or Atom `id`, link, and a date (RFC 822 for RSS, RFC 3339 for Atom).
- Keep GUIDs permanent; use the canonical URL or an internal id, never a changing slug.
- Set `Content-Type` to `application/rss+xml` or `application/atom+xml` with UTF-8, an `ETag` and `Last-Modified`, and answer conditional requests with 304.
- Escape XML properly or use a library; put HTML in `content:encoded` or CDATA; make links absolute.
- Advertise discovery with `<link rel="alternate" type="application/rss+xml">` in the page head.
- When consuming, send conditional GET, honor `Cache-Control` and 429 or `Retry-After`, back off on errors, set a User-Agent, and a timeout and size cap.
- Dedupe items by guid, falling back to link or a content hash; treat date-less items by first-seen time.
- Sanitize item HTML before display and resolve relative URLs against the feed or item base.
- Parse leniently (feedparser handles broken feeds); cap items per fetch.

## Avoid
- Changing GUIDs when titles or URLs change: readers show duplicates. Keep ids fixed.
- Local-time or ISO dates in RSS `pubDate`: readers reject or misorder. Use RFC 822.
- Unescaped `&` and control characters in XML: the feed breaks. Use an XML writer.
- Fetching every minute without conditional GET: you get banned and waste bandwidth.
- Rendering item HTML unsanitized: XSS from third-party feeds. Sanitize.
- Fetching feed URLs supplied by users without limits: SSRF. Block private addresses and cap redirects.

## Review
- [ ] Feed validates and is well-formed.
- [ ] GUIDs are permanent.
- [ ] Conditional GET is implemented on both sides.
- [ ] Item HTML is sanitized.
- [ ] Outbound fetches have SSRF protection and limits.
