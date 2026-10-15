---
name: beautifulsoup
title: Beautiful Soup
area: python
tags: [python, scraping, html, parsing, beautifulsoup, lxml]
detect: [dep:beautifulsoup4, dep:bs4, dep:lxml]
related: [httpx, scrapy, selenium, pytest]
---
Beautiful Soup: parse HTML with an explicit parser, select with CSS, and handle missing nodes without crashing.

## Verify
- `python -c "from bs4 import BeautifulSoup; print(BeautifulSoup('<p>x</p>', 'html.parser').p.text)"`: the package imports (install `beautifulsoup4`, import `bs4`).
- `pytest -q`: parser tests against saved HTML fixtures.
- `python -c "import lxml.html"`: the fast parser is installed when you choose `"lxml"`.

## Test first
Save real pages as fixtures and test the parser offline, including missing fields.
```python
from pathlib import Path
from app.parse import parse_product

def test_parses_fixture():
    html = Path("tests/fixtures/product.html").read_text()
    p = parse_product(html)
    assert p == {"name": "Widget", "price": 9.99}

def test_missing_price_is_none():
    assert parse_product("<h1>Widget</h1>")["price"] is None
```

## Do
- Name the parser: `BeautifulSoup(html, "lxml")` for speed or `"html.parser"` for no extra dependency. Results can differ on broken HTML, so pin one.
- Select with CSS: `soup.select("div.card > a[href]")` and `soup.select_one("h1")`.
- Guard `None`: `el = soup.select_one(...)`, then `el.get_text(strip=True) if el else None`.
- Read attributes with `el.get("href")` (returns `None` if absent) rather than `el["href"]`.
- Resolve links with `urllib.parse.urljoin(base_url, href)`.
- Pass bytes (`response.content`) so the parser detects encoding.
- Use `SoupStrainer` or `parse_only` to parse only the parts you need on huge pages.
- Fetch with `httpx` or `requests` with timeouts, a User-Agent, rate limits, and respect robots.txt and terms.

## Avoid
- Chained attribute access (`soup.div.a.text`): `AttributeError: NoneType` when a node is missing. Use `select_one` and guards.
- The deprecated camelCase API (`findAll`, `findNext`, `.text` aside): use `find_all`, `select`.
- Regex on raw HTML for structure: brittle. Parse, then select.
- Using Beautiful Soup on JavaScript-rendered pages: you get an empty shell. Find the JSON API, or use a browser automation tool.
- Unbounded requests without timeout: hangs. Always set `timeout=`.
- Trusting scraped text in SQL or HTML output: inject risk. Parameterize and escape.
- Assuming a selector survives site changes silently: add a test that fails when the expected count is zero.

## Review
- [ ] Parser is named explicitly and input is bytes.
- [ ] Every lookup handles a missing element.
- [ ] Tests use saved fixtures, with no live network.
- [ ] Requests have timeouts, delays and a clear User-Agent.
