---
name: puppeteer
title: Puppeteer
area: node
tags: [puppeteer, browser, headless, scraping, pdf, screenshots]
detect: [dep:puppeteer, dep:puppeteer-core]
related: [cheerio, axios, vitest, jest]
---
Puppeteer automation: always close browsers, wait on conditions not time, sandbox correctly in containers, tests that clean up.

## Verify
- `npx puppeteer browsers install chrome`: the pinned browser is downloaded (needed in CI and Docker).
- `node -e "require('puppeteer').launch().then(b=>b.close())"`: launch and close work in this environment.
- `npx tsc --noEmit`: `Page`, `ElementHandle` and evaluate callbacks type-check.
- `npx vitest run`: integration tests with generous timeouts, serving fixtures from a local server.

## Test first
Test against a local fixture page, with guaranteed cleanup.
```ts
import puppeteer, { Browser } from 'puppeteer';

let browser: Browser;
beforeAll(async () => { browser = await puppeteer.launch({ headless: true }); });
afterAll(async () => { await browser.close(); });

test('renders the heading', async () => {
  const page = await browser.newPage();
  await page.setContent('<h1 id="t">Hi</h1>');
  expect(await page.$eval('#t', el => el.textContent)).toBe('Hi');
  await page.close();
}, 30_000);
```

## Do
- Wrap work in `try/finally` and `await browser.close()`; reuse one browser and open pages per task.
- Wait for the condition: `page.waitForSelector`, `page.waitForResponse`, `page.waitForFunction`, or locators (`page.locator(sel).click()`).
- Navigate with `page.goto(url, { waitUntil: 'networkidle0', timeout })` only when it matches the page; prefer waiting for a selector.
- Set `page.setViewport`, `setUserAgent` and timeouts (`page.setDefaultTimeout`) deliberately.
- In Docker run as non-root with `--no-sandbox` only if you cannot enable user namespaces; prefer a seccomp profile or a sandboxed image.
- Use `page.pdf({ printBackground: true, format })` and `page.screenshot({ fullPage, type })` for output.
- Cap concurrency with a pool or `p-limit`; each page consumes memory.
- Block images, fonts and trackers with request interception when scraping.

## Avoid
- `page.waitForTimeout`: removed in recent versions and flaky. Wait for a selector or response.
- Leaking browsers when a step throws: zombie Chrome processes. Use `finally`.
- Using `--no-sandbox` by default on user-supplied pages: escape risk. Only for trusted content in an isolated container.
- Passing outer variables into `page.evaluate` closures: they are not in scope. Pass arguments as extra parameters.
- Scraping pages with attacker-controlled URLs without allowlisting: SSRF into internal hosts.
- `page.$eval` on a missing selector: throws; check with `page.$` first when optional.

## Review
- [ ] Every browser and page is closed on all paths.
- [ ] No fixed sleeps; waits are condition-based.
- [ ] Sandbox flags are justified for the environment.
- [ ] URLs from users are validated.
- [ ] Concurrency bounded and timeouts set.
