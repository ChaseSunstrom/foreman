// fm smoke's crawl (T-0417): node smoke_web.cjs <playwright package dir> <url> <screenshot dir>
// Opens the page at desktop and phone width, visits every visible tab (or, with none, the nav links), and prints one
// JSON line: {"views": [...], "defects": [{"where", "what"}], "notes": [...]}: what a user would see go wrong.
const { chromium } = require(process.argv[2]);
const [url, out] = process.argv.slice(3);
const path = require("path");

// review: a Tailwind `placeholder:` class or a permanent spinner button is no stuck load; aria-busy and skeletons are
const PLACEHOLDERS = '[aria-busy="true"], [class*="skeleton" i], [class*="shimmer" i], ' +
  '[class*="loading" i]:not(input, button, select, textarea, a)';
const SETTLE_MS = 5000;
const DEADLINE = Date.now() + 200000;  // under fm smoke's 240 s: print what was found rather than lose it all
const VIEW_MS = 30000;  // T-0420: a view (or a load) that takes longer has stopped responding
const HUNG = new Error("hung");

const views = [], defects = [], notes = [], seen = new Set();
const add = (where, what) => {
  const key = where.split(" ")[0] + "|" + what;  // one report per viewport, at the first view it shows in
  if (!seen.has(key)) { seen.add(key); defects.push({ where, what: what.slice(0, 300) }); }
};
const finish = () => { console.log(JSON.stringify({ views, defects, notes })); process.exit(0); };
// T-0420: a frozen page leaves Playwright calls that never return; whatever happens, print what was found
setTimeout(() => { notes.push(`stopped at the time limit after ${views.length} views`); finish(); }, DEADLINE + 15000 - Date.now());
const withTimeout = (p, ms) => Promise.race([p, new Promise((_, no) => setTimeout(() => no(HUNG), ms))]);

(async () => {
  const host = new URL(url).hostname;
  const ours = u => { try { return new URL(u).hostname === host; } catch (e) { return false; } };  // any port: its API
  const browser = await chromium.launch();
  for (const [label, viewport] of [["desktop", { width: 1440, height: 900 }], ["phone", { width: 390, height: 844 }]]) {
    let where = `${label} start`, ctx;
    try { await withTimeout((async () => {  // a viewport gets its views' share of the deadline, then is abandoned
    ctx = await browser.newContext({ viewport, ignoreHTTPSErrors: true });
    const page = await ctx.newPage();
    page.on("pageerror", e => add(where, `page error: ${e.message}`));
    page.on("console", m => {
      if (m.type() === "error" && !m.text().startsWith("Failed to load resource")) add(where, `console error: ${m.text()}`);
    });
    page.on("response", r => {  // 4xx from the app's own host (any port), 5xx from anywhere
      const u = new URL(r.url());
      if ((r.status() >= 500 || (r.status() >= 400 && ours(r.url()))) && u.pathname !== "/favicon.ico")
        add(where, `HTTP ${r.status()} ${ours(r.url()) ? u.pathname : u.origin + u.pathname}`);
    });
    page.on("requestfailed", r => {
      const err = (r.failure() || {}).errorText || "";
      if (ours(r.url()) && !err.includes("ERR_ABORTED")) add(where, `request failed: ${new URL(r.url()).pathname} ${err}`);
    });
    try {
      await page.goto(url, { waitUntil: "load", timeout: 30000 });
    } catch (e) {
      add(where, `did not load (is the server running?): ${e.message.split("\n")[0]}`);
      return;
    }
    const check = async () => {
      views.push(where);
      let stuck = [];
      for (let t = 0; t <= SETTLE_MS; t += 500) {  // placeholders get SETTLE_MS to resolve
        stuck = await page.evaluate(sel => [...document.querySelectorAll(sel)].filter(e => {
          const r = e.getBoundingClientRect(), s = getComputedStyle(e);
          return r.width > 2 && r.height > 2 && s.visibility !== "hidden" && s.display !== "none" && s.opacity !== "0";
        }).map(e => {
          const named = e.closest("[aria-label]");
          return named ? named.getAttribute("aria-label") : `${e.tagName.toLowerCase()}.${String(e.className).split(" ")[0]}`;
        }), PLACEHOLDERS);
        if (!stuck.length) break;
        await page.waitForTimeout(500);
      }
      for (const s of new Set(stuck)) add(where, `loading placeholder still showing after ${SETTLE_MS / 1000} s (${s})`);
      const found = await page.evaluate(() => {
        // review: a 1 px clipped announcer (Next.js's route announcer is role=alert) isn't on screen
        const visible = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
          return r.width > 2 && r.height > 2 && s.visibility !== "hidden" && s.clip === "auto"; };
        const name = e => (e.getAttribute("aria-label") || e.innerText || e.tagName).trim().split("\n")[0].slice(0, 40);
        const res = [];
        for (const a of document.querySelectorAll('[role="alert"], [role="alertdialog"]'))
          if (visible(a) && a.innerText.trim()) res.push(`alert shown: ${a.innerText.trim().replace(/\s+/g, " ")}`);
        const W = window.innerWidth, H = window.innerHeight;
        if (document.documentElement.scrollWidth > W + 1)
          res.push(`page wider than the screen (${document.documentElement.scrollWidth} px > ${W} px)`);
        // fixed controls only (sticky headers and columns meet by design), outside an open dialog
        const fixed = [...document.querySelectorAll("body *")].filter(e => {
          const r = e.getBoundingClientRect();
          return getComputedStyle(e).position === "fixed" && visible(e) && r.width * r.height < 0.6 * W * H &&
            !e.closest('[role="dialog"], [aria-modal="true"]');
        });
        for (let i = 0; i < fixed.length; i++) for (let j = i + 1; j < fixed.length; j++) {
          const a = fixed[i], b = fixed[j];
          if (a.contains(b) || b.contains(a)) continue;
          const r = a.getBoundingClientRect(), q = b.getBoundingClientRect();
          const w = Math.min(r.right, q.right) - Math.max(r.left, q.left), h = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
          if (w > 2 && h > 2) res.push(`"${name(a)}" and "${name(b)}" overlap`);
        }
        return res;
      });
      for (const f of found) add(where, f);
      await page.screenshot({ path: path.join(out, `${views.length}-${where.replace(/[^\w]+/g, "-").slice(0, 60)}.png`) });
    };
    await withTimeout(check(), VIEW_MS);
    const tabs = [];
    for (const tab of (await page.getByRole("tab").all()).slice(0, 24))
      if (await tab.isVisible()) tabs.push(tab);
    if (tabs.length) {
      for (const tab of tabs) {
        if (Date.now() > DEADLINE) break;
        where = `${label} tab ${((await tab.innerText()).trim().split("\n")[0] || "unnamed").slice(0, 40)}`;
        try {
          await tab.click({ timeout: 3000 });
        } catch (e) {
          add(where, `tab can't be clicked: ${e.message.split("\n")[0]}`);
          continue;
        }
        await withTimeout(check(), VIEW_MS);
      }
    } else {  // review: an app without role=tab is still more than its start view
      const links = await page.evaluate(() => [...new Set([...document.querySelectorAll('nav a[href], [role="navigation"] a[href]')]
        .map(a => a.href).filter(h => h.startsWith(location.origin) && h.split("#")[0] !== location.href.split("#")[0]))]);
      if (!links.length) notes.push(`${label}: no tabs or nav links found; only the start view was checked`);
      for (const href of links.slice(0, 10)) {
        if (Date.now() > DEADLINE) break;
        where = `${label} page ${new URL(href).pathname.slice(0, 40)}`;
        try {
          await page.goto(href, { waitUntil: "load", timeout: 30000 });
        } catch (e) {
          add(where, `did not load: ${e.message.split("\n")[0]}`);
          continue;
        }
        await withTimeout(check(), VIEW_MS);
      }
    }
    })(), Math.max(VIEW_MS, (DEADLINE - Date.now()) / (label === "desktop" ? 2 : 1))); } catch (e) {
      add(where, e === HUNG ? `the page stopped responding (no answer for ${VIEW_MS / 1000} s)` : `crawl error: ${e.message}`);
    }
    if (ctx) ctx.close().catch(() => {});  // not awaited: a frozen renderer may never answer
    if (Date.now() > DEADLINE) { notes.push(`stopped at the time limit after ${views.length} views`); break; }
  }
  await withTimeout(browser.close(), 10000).catch(() => {});
  finish();
})().catch(e => { add("smoke", `crawl crashed: ${e.message}`); finish(); });
