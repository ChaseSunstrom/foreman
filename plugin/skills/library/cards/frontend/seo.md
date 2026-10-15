---
name: seo
title: Technical SEO
area: frontend
tags: [seo, meta, sitemap, structured-data, open-graph, crawling]
detect: [dep:next-sitemap, dep:react-helmet-async, dep:@unhead/vue, dep:astro-seo, dep:schema-dts, file:robots.txt, file:sitemap.xml]
related: [web-performance, accessibility, i18n, pwa]
---
Crawlable, indexable pages: server-rendered content, correct metadata, canonical URLs, sitemap and structured data.

## Verify
- `curl -s https://example.com/page | grep -iE "<title>|rel=\"canonical\"|name=\"description\"|name=\"robots\""`: metadata is in the initial HTML, not injected later.
- `curl -sI https://example.com/old`: status and `Location` for redirects; `X-Robots-Tag` headers.
- `curl -s https://example.com/robots.txt`: it allows what it should and lists the sitemap.
- `xmllint --noout public/sitemap.xml`: sitemap is well-formed.

## Test first
Assert the head of the server-rendered HTML, with JavaScript disabled.
```ts
import { test, expect } from '@playwright/test';

test.use({ javaScriptEnabled: false });

test('product page has unique title, canonical and JSON-LD', async ({ page }) => {
  await page.goto('/products/widget');
  await expect(page).toHaveTitle(/Widget/);
  await expect(page.locator('link[rel=canonical]')).toHaveAttribute('href', /\/products\/widget$/);
  const ld = await page.locator('script[type="application/ld+json"]').textContent();
  expect(JSON.parse(ld!)['@type']).toBe('Product');
});
```

## Do
- Render content on the server or at build time (SSR, SSG); crawlers see it without running scripts.
- One unique `<title>` and meta description per URL; one `h1`.
- Absolute `<link rel="canonical">` on every page, matching the preferred host and protocol.
- Use real `<a href>` links for navigation so crawlers can follow them.
- Provide `sitemap.xml` with canonical URLs and `lastmod`; reference it in `robots.txt`.
- Add JSON-LD structured data (`Product`, `Article`, `BreadcrumbList`) that matches visible content.
- Open Graph and `twitter:card` tags with an absolute image URL at least 1200x630.
- `hreflang` pairs, reciprocal and including self, for localized pages.
- Return 404 or 410 for gone pages and 301 for permanent moves.
- Use `noindex` for staging, search results and thin pages.

## Avoid
- Client-only rendering of main content: may be indexed late or empty. Use SSR or prerender.
- Blocking a page in `robots.txt` and also expecting `noindex` to work: the crawler never sees the tag. Allow crawling, use `noindex`.
- A soft 404 (a 200 with "not found" text): wastes crawl and pollutes the index. Return 404.
- Duplicate URLs via trailing slash, query params, or case: split ranking. Canonicalize and redirect.
- Staging site left indexable: add auth or `noindex` and exclude from sitemaps.
- Structured data for content not on the page: risks a manual action. Mirror visible content.
- Hash-based routes (`#/page`): not separate URLs. Use the History API.

## Review
- [ ] Title, description, canonical, and `h1` unique and present in raw HTML.
- [ ] Redirects are single-hop 301s; errors return real 4xx codes.
- [ ] Sitemap and robots reflect only indexable canonical URLs.
- [ ] Structured data validates and matches the page.
- [ ] Core Web Vitals pass on key templates.
