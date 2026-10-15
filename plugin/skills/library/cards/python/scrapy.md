---
name: scrapy
title: Scrapy
area: python
tags: [python, scraping, crawler, scrapy, spiders, pipelines]
detect: [dep:scrapy, dep:Scrapy, file:scrapy.cfg]
related: [pytest, httpx, pydantic]
---
Scrapy crawlers: spiders, selectors, items and pipelines, middlewares, politeness settings.

## Verify
- `scrapy list`: the project loads and spiders register.
- `scrapy check SPIDER`: runs the spider contracts (`@url`, `@returns`, `@scrapes`) in its docstrings.
- `scrapy parse --spider=SPIDER -c parse_item URL`: runs one callback on one live page and prints items and requests.
- `scrapy crawl SPIDER -O out.json`: a bounded run (add `-s CLOSESPIDER_PAGECOUNT=5`) overwriting the output file.

## Test first
Parse saved HTML; no network. Fixtures live in `tests/fixtures/`.
```python
from scrapy.http import HtmlResponse
from app.spiders.shop import ShopSpider

def test_parse_item_extracts_price():
    body = open("tests/fixtures/item.html", "rb").read()
    resp = HtmlResponse(url="http://t/item/1", body=body, encoding="utf-8")
    items = list(ShopSpider().parse_item(resp))
    assert items[0]["price"] == "19.99"
```

## Do
- Extract with `response.css(...)` or `.xpath(...)` and `.get()`/`.getall()`; use `response.follow(href, callback)` for links.
- Yield items as `scrapy.Item`, dataclasses or dicts; validate and clean them in item pipelines.
- Set `ROBOTSTXT_OBEY = True`, a descriptive `USER_AGENT`, `DOWNLOAD_DELAY` or `AUTOTHROTTLE_ENABLED = True`, and `CONCURRENT_REQUESTS_PER_DOMAIN`.
- Keep `HTTPCACHE_ENABLED = True` locally so reruns do not hit the site.
- Pass state between callbacks with `cb_kwargs`, not globals.
- Dedupe by relying on the default dupefilter; set `dont_filter=True` only deliberately.
- Handle failures with `errback=` and log them.
- Use `scrapy-playwright` or similar only for pages that need JavaScript.

## Avoid
- `requests` or blocking sync calls inside callbacks: stalls the Twisted reactor. Yield `scrapy.Request`.
- `.extract()`/`.extract_first()` in new code: older aliases. Use `.getall()` and `.get()`.
- `response.css(...).get()` assumed non-None: `None` on miss crashes later. Pass `default=""` or check.
- Disabling `ROBOTSTXT_OBEY` or hammering a site with no delay: bans and legal exposure. Throttle.
- Storing cookies, tokens or credentials in spider source: read from settings or env.
- Logic spread across callbacks with no pagination stop: infinite crawls. Bound by depth (`DEPTH_LIMIT`) or an explicit next-page check.
- Mutating `item` in a later callback after yielding it: shared reference bugs. Yield a fresh item.

## Review
- [ ] Callbacks are tested against saved HTML fixtures and cover a missing-field page.
- [ ] Politeness settings (robots, delay or autothrottle, user agent) are set.
- [ ] Pipelines validate and normalize items; duplicates are handled by key.
- [ ] No blocking I/O in callbacks or pipelines (use `deferToThread` where needed).
- [ ] Crawls are bounded and failures are logged via errbacks.
