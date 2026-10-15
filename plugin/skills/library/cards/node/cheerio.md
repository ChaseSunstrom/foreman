---
name: cheerio
title: Cheerio
area: node
tags: [cheerio, html, parsing, scraping, selectors, dom]
detect: [dep:cheerio]
related: [puppeteer, axios, undici, vitest]
---
Cheerio HTML parsing: jQuery-style selectors on static markup, fixture-driven extraction, no JavaScript execution.

## Verify
- `npx tsc --noEmit`: `CheerioAPI` and `Element` types compile (import types from `cheerio`).
- `node -e "const c=require('cheerio');console.log(c.load('<p>x</p>')('p').text())"`: parses and prints `x`.
- `npx vitest run`: extractors tested against saved HTML fixtures.
- `grep -rn "require('cheerio')" src`: confirms CJS usage matches the module setup.

## Test first
Save a real page as a fixture and assert the extractor output.
```ts
import { readFileSync } from 'node:fs';
import { parseProducts } from '../src/parse';

test('extracts name and numeric price, skipping malformed rows', () => {
  const html = readFileSync('test/fixtures/list.html', 'utf8');
  const items = parseProducts(html);
  expect(items[0]).toEqual({ name: 'Widget', price: 9.99 });
  expect(items.every(i => Number.isFinite(i.price))).toBe(true);
});
```

## Do
- Load with `import * as cheerio from 'cheerio'; const $ = cheerio.load(html)`; the default export is deprecated.
- Scope queries: `$(row).find('.price')` instead of global selectors per row.
- Use `.text().trim()`, `.attr('href')`, `.data()`, `.map((i, el) => ...).get()` to turn nodes into plain arrays.
- Resolve relative links with `new URL(href, baseUrl)`.
- Parse numbers explicitly and strip currency and whitespace; return `undefined` on failure.
- Return plain typed objects from extractors; keep fetching and parsing separate functions.
- Use `cheerio.load(html, null, false)` to parse a fragment without html/body wrappers.
- For JS-rendered pages, fetch the underlying JSON endpoint or use a browser tool.

## Avoid
- Expecting JavaScript-rendered content: Cheerio only sees served HTML. Use the API behind the page or Puppeteer.
- `.text()` on a container without trimming: includes nested whitespace and script text.
- Selectors tied to generated class names (hashed CSS modules): break on every deploy. Use structure or data attributes.
- Using `$(...)` results as arrays directly: they are cheerio objects. Call `.toArray()` or `.get()`.
- Inserting scraped HTML into pages with `.html()` output unsanitized: XSS. Escape or sanitize.
- Parsing untrusted HTML of unbounded size: cap the response size before loading.

## Review
- [ ] Extractors are pure functions of an HTML string with fixtures.
- [ ] Missing nodes yield explicit results, not crashes or `NaN`.
- [ ] Links resolved against the base URL.
- [ ] Selectors are stable rather than hashed class names.
- [ ] Response size and encoding handled before parsing.
