// fm smoke's crawl (T-0417): node smoke_web.cjs <playwright package dir> <url> <screenshot dir> [profile]
// Opens the page at desktop and phone width, visits every visible tab (or, with none, the nav links), and prints one
// JSON line: {"views": [...], "defects": [{"where", "what"}], "notes": [...]}: what a user would see go wrong.
// T-1509: with no profile it first shoots the start page's frame matrix (ui/visual-qa.md) into <dir>/frames, whose
// findings come apart as "frame_findings" (fm smoke fails on them only when strict); a profile (PROFILES) crawls under
// one hostile condition instead. Every screenshot is named after its view, not a counter, so a
// receipt can point at it. A Playwright whose browser isn't installed prints {"skipped": why}: nothing is installed.
const path = require("path");
const fs = require("fs");

// review: a Tailwind `placeholder:` class or a permanent spinner button is no stuck load; aria-busy and skeletons are
const PLACEHOLDERS = '[aria-busy="true"], [class*="skeleton" i], [class*="shimmer" i], ' +
  '[class*="loading" i]:not(input, button, select, textarea, a)';
const SETTLE_MS = 5000;
const DEADLINE = Date.now() + 200000;  // under fm smoke's 240 s: print what was found rather than lose it all
const VIEW_MS = 30000;  // T-0420: a view (or a load) that takes longer has stopped responding
const FRAMES_MS = 60000;  // the frame matrix's share of the deadline
const HUNG = new Error("hung");
const SIZES = [[360, 800], [768, 1024], [1440, 900]];  // visual-qa.md's frame matrix: × THEMES, + reduced motion at 360
const THEMES = ["light", "dark"];
const NOW = new Date("2026-01-15T10:00:00Z");  // the frozen profile's "now" (visual-qa.md's fixture)
const FRAME_MAX_H = 8000;  // a frame's cap in px each way: an endless feed is not an endless PNG
const JUNK = /\bundefined\b|\bNaN\b|\bnull\b|Invalid Date|\[object Object\]|lorem ipsum/i;
const MOTION_FRAMES = 5;  // motion: frames 250 ms apart per view

const run = { url: "", out: "", profile: "" };
const views = [], defects = [], notes = [], framed = [], seen = new Set(), taken = new Set();
const add = (where, what) => {
  const key = where.split(" ")[0] + "|" + what;  // one report per viewport, at the first view it shows in
  if (!seen.has(key)) { seen.add(key); defects.push({ where, what: what.slice(0, 300) }); }
};
const frameFinding = (where, what) => { if (!framed.some(f => f.what === what)) framed.push({ where, what }); };
const slug = s => {  // letters in any script stay (a tab named 设置 is not "desktop-tab"), cut by whole characters
  const cs = [...s.replace(/[^\p{L}\p{M}\p{N}_]+/gu, "-").replace(/^-+|-+$/g, "")].slice(0, 60);
  while (Buffer.byteLength(cs.join("")) > 180) cs.pop();  // a file name's 255 bytes, with room for -2-motion-4.png
  return cs.join("").replace(/-+$/, "") || "home";
};
const shotStem = where => {  // the view's own name, numbered only when two views share one
  let stem = path.join(run.out, slug(where)), i = 1;
  while (taken.has(stem)) stem = path.join(run.out, `${slug(where)}-${++i}`);
  taken.add(stem);
  return stem;
};
const ours = u => { try { return new URL(u).hostname === new URL(run.url).hostname; } catch (e) { return false; } };  // any port: its API
const withTimeout = (p, ms) => Promise.race([p, new Promise((_, no) => setTimeout(() => no(HUNG), ms))]);
const snap = (page, opts = {}) => page.screenshot(opts).catch(async e => {  // headless Chromium now and then has no
  if (!/Unable to capture screenshot/.test(e.message)) throw e;            // frame to give (a filtered page): once more
  await page.waitForTimeout(500);
  return page.screenshot(opts);
});
const outOfTime = (p, where) => p.patient  // offline and slow 3G spend their budget by design: say so, it's no hang
  ? notes.push(`${where}: ran out of time on ${p.name}; the views after it weren't checked`)
  : add(where, `the page stopped responding (no answer for ${VIEW_MS / 1000} s)`);

// Hostile profiles. Hooks: setup(ctx, page) before the first load, loaded(ctx, page, label, ms) after it, view(page,
// where, stem) per view once it settles (before its checks and screenshot), end() before the report; quiet: failed
// requests, console errors and pages that don't load are expected, and an alert saying so is right (a note, not a
// defect; an uncaught page error still is one); loadMs and settleMs stretch the waits; patient: running out of time
// is a note (outOfTime), not a hang.
const LONG = "Pneumonoultramicroscopicsilicovolcanoconiosis".repeat(2);  // 90 letters and nowhere to break
const RTL = "مرحبا بالعالم، هذا سطر طويل يُقرأ من اليمين إلى اليسار";
const HUGE = "12345678901234567890";
function torture([long, rtl, huge]) {  // in the page: its own text, made hostile; the boxes it then spills out of
  const done = window.__fmTortured || (window.__fmTortured = new WeakSet());  // a later view: only the new text
  const skip = "script, style, noscript, template, textarea, code, pre, svg, [role=tab]";  // tabs name the views
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), hit = new Set();
  let i = 0;
  for (let n = walk.nextNode(); n && hit.size < 2000; n = walk.nextNode()) {
    const el = n.parentElement;
    if (done.has(n) || !n.data.trim() || !el || el.closest(skip)) continue;
    done.add(n);
    if (/\d/.test(n.data)) n.data = n.data.replace(/\d[\d.,]*/g, huge);
    else if (i++ % 2 === 0) n.data = n.data.trimEnd() + " " + long;
    else n.data = rtl;
    hit.add(el);
  }
  const spill = new Set();
  for (let e of hit) {
    while (e && e !== document.body && /^(inline|contents)$/.test(getComputedStyle(e).display)) e = e.parentElement;
    if (!e || e === document.body || !e.clientWidth) continue;
    const s = getComputedStyle(e);
    if (e.scrollWidth > e.clientWidth + 1 && s.overflowX === "visible" && s.visibility !== "hidden")
      spill.add(e.getAttribute("aria-label") || e.tagName.toLowerCase() + (e.classList[0] ? "." + e.classList[0] : ""));
  }
  return [...spill].slice(0, 5);
}
let emptied = 0;
const hollow = v => Array.isArray(v) ? [] : v && typeof v === "object"
  ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, hollow(x)])) : v;
async function emptyJson(route) {  // the app's own JSON with every list emptied: its real empty states
  const req = route.request();
  let res = null, body;
  try {  // a handler that throws is an unhandled rejection in node: every path ends answered or swallowed
    if (!ours(req.url()) || !["fetch", "xhr"].includes(req.resourceType())) return await route.continue();
    res = await route.fetch();
    if (!/json/i.test(res.headers()["content-type"] || "")) return await route.fulfill({ response: res });
    try { body = hollow(JSON.parse(await res.text())); } catch (e) { return await route.fulfill({ response: res }); }
    emptied++;
    const headers = { ...res.headers() };  // route.fetch decoded the body: its old length and encoding no longer hold
    for (const h of ["content-length", "content-encoding", "transfer-encoding"]) delete headers[h];
    return await route.fulfill({ status: res.status(), headers, json: body });
  } catch (e) {
    return (res ? route.fulfill({ response: res }) : route.continue()).catch(() => {});
  }
}
// Colour-vision deficiencies as an SVG colour matrix on the whole page: Machado, Oliveira and Fernandes (2009),
// severity 1, in linear RGB (an SVG filter's own space); achromatopsia keeps luminance only.
const CVD = {
  deuteranopia: "0.367322 0.860646 -0.227968 0.280085 0.672501 0.047413 -0.011820 0.042940 0.968881",
  protanopia: "0.152286 1.052583 -0.204868 0.114503 0.786281 0.099216 -0.003882 -0.048116 1.051998",
  tritanopia: "1.255528 -0.076749 -0.178779 -0.078411 0.930809 0.147602 0.004733 0.691367 0.303900",
  achromatopsia: "0.2126 0.7152 0.0722 0.2126 0.7152 0.0722 0.2126 0.7152 0.0722",
};
const matrix = m => { const v = m.split(" "); return [0, 3, 6].map(r => `${v[r]} ${v[r + 1]} ${v[r + 2]} 0 0 `).join("") + "0 0 0 1 0"; };
function seeAs(values) {  // in the page, before its scripts: the filter on <html> (which keeps fixed elements fixed)
  const put = () => {
    if (document.getElementById("fm-cvd")) return;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("style", "position:absolute;width:0;height:0;overflow:hidden");
    svg.setAttribute("aria-hidden", "true");
    svg.innerHTML = `<filter id="fm-cvd" color-interpolation-filters="linearRGB"><feColorMatrix type="matrix" values="${values}"/></filter>`;
    document.documentElement.appendChild(svg);  // not in body, which an app may re-render
    document.documentElement.style.setProperty("filter", "url(#fm-cvd)", "important");
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", put); else put();
}
const cvd = name => ({ setup: (ctx, page) => page.addInitScript(seeAs, matrix(CVD[name])) });
function freeze() {  // in the page: CSS animations and transitions held still
  const put = () => {
    const s = document.createElement("style");
    s.textContent = "*, *::before, *::after { animation-play-state: paused !important; transition: none !important; " +
      "caret-color: transparent !important; scroll-behavior: auto !important }";
    document.documentElement.appendChild(s);
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", put); else put();
}
// T-1627: in the page, under freeze(): each paused motion-NAME animation (fm motion compile's @keyframes) seeked to 0,
// eighths of its own duration and its end, each animated property read as numbers ("none" transform as the identity);
// fm motion verify holds them to the score's duration and curve. Transitions are off under freeze(), so not sampled.
function sampleMotion(where) {
  const nums = v => ((v.trim() === "none" ? "matrix(1, 0, 0, 1, 0, 0)" : v).match(/-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?/gi) || []).map(Number);
  const skip = new Set(["offset", "computedOffset", "easing", "composite"]), out = [], notes = [];
  const all = document.getAnimations();  // reduced-motion-NAME forms play only under reduced motion: not these
  if (all.length > 50) notes.push(`${where}: sampled the first 50 of ${all.length} animations`);
  for (const a of all.slice(0, 50)) {
    const e = a.effect, name = a.animationName || "";
    if (!name.startsWith("motion-") || !e || !e.target) continue;
    let t = null, was = null;
    try {
      t = e.getTiming(); was = a.currentTime;
      const dur = Number(t.duration) || 0;
      if (!(dur > 0 && dur <= 20000)) continue;
      const props = [...new Set(e.getKeyframes().flatMap(k => Object.keys(k)))].filter(k => !skip.has(k))
        .map(k => (k.startsWith("--") ? k : k.replace(/[A-Z]/g, c => "-" + c.toLowerCase()))).slice(0, 8);
      // one forward iteration, held at both ends: a repeating or reversed animation seeked to its duration would be
      // back at its start (review)
      e.updateTiming({ iterations: 1, iterationStart: 0, direction: "normal", fill: "both" });
      const read = ms => {
        a.currentTime = (t.delay || 0) + ms;
        const s = getComputedStyle(e.target, e.pseudoElement || null);
        return props.map(p => nums(s.getPropertyValue(p)).slice(0, 16));
      };
      const from = read(0), to = read(dur), at = [1, 2, 3, 4, 5, 6, 7].map(k => [dur * k / 8, read(dur * k / 8)]);
      props.forEach((p, i) => out.push({ motion: name.slice(7, 71), property: p, where, from: from[i], to: to[i],
                                         at: at.map(([ms, v]) => [ms, v[i]]) }));
    } catch (err) {
      notes.push(`${where}: ${name.slice(0, 71)}: not sampled: ${String(err && err.message || err).slice(0, 120)}`);
    } finally {
      try {
        if (t) e.updateTiming({ iterations: t.iterations, iterationStart: t.iterationStart || 0,
                                direction: t.direction, fill: t.fill });
        if (was !== null) a.currentTime = was;
      } catch (err) { /* the page took it back: nothing to restore */ }
    }
  }
  return { samples: out, notes };
}
const motionSamples = [], motionNotes = [];
const PROFILES = {
  torture: {
    view: async (page, where) => {
      for (const box of await page.evaluate(torture, [LONG, RTL, HUGE]))
        add(where, `text runs out of its box: ${box} (a 90-letter word, a right-to-left run or a 20-digit number)`);
    },
  },
  empty: {
    setup: ctx => ctx.route("**/*", emptyJson),
    end: () => { if (!emptied) notes.push("empty: nothing was emptied: no JSON came from the app's own host (lists that " +
                                          "come with the HTML need an empty fixture)"); },
  },
  offline: {  // after the first load: the app is open, then the network goes; each view gets 3 s to notice
    loaded: ctx => ctx.setOffline(true), view: page => page.waitForTimeout(3000), quiet: true, patient: true,
  },
  slow3g: {
    setup: async (ctx, page) => {  // DevTools' Slow 3G: 2 s latency, 50 KB/s each way
      const cdp = await ctx.newCDPSession(page);
      await cdp.send("Network.enable");
      await cdp.send("Network.emulateNetworkConditions", { offline: false, latency: 2000, downloadThroughput: 51200,
                                                            uploadThroughput: 51200 });
    },
    loaded: (ctx, page, label, ms) => { notes.push(`${label}: the start page loaded in ${(ms / 1000).toFixed(1)} s on slow 3G`); },
    loadMs: 90000, settleMs: 15000, patient: true,
  },
  deuteranopia: cvd("deuteranopia"), protanopia: cvd("protanopia"), tritanopia: cvd("tritanopia"),
  achromatopsia: cvd("achromatopsia"),
  frozen: {
    setup: async (ctx, page) => {
      if (page.clock) await page.clock.setFixedTime(NOW);
      else notes.push("frozen: this Playwright has no page.clock (1.45 or later): the time isn't fixed");
      await page.addInitScript(freeze);
    },
    view: async (page, where) => {
      const a = await snap(page);
      await page.waitForTimeout(1000);
      if (!a.equals(await snap(page)))
        notes.push(`${where}: still changes with the clock frozen and animations paused (a canvas, video or timer)`);
      if (motionSamples.length >= 500) {  // after the stillness check: seeking moves the page
        if (!motionNotes.some(n => n.startsWith("stopped sampling"))) motionNotes.push(`stopped sampling at 500 samples, before ${where}`);
        return;
      }
      try {
        const got = await page.evaluate(sampleMotion, where);
        motionSamples.push(...got.samples);
        motionNotes.push(...got.notes);
      } catch (e) {  // a sampler that throws costs its samples, never the frozen crawl
        motionNotes.push(`${where}: motion sampling failed: ${e.message.split("\n")[0]}`);
      }
    },
  },
  motion: {
    view: async (page, where, stem) => {
      stem = stem || path.join(run.out, slug(where));
      let prev = null, moved = 0;
      for (let i = 0; i < MOTION_FRAMES; i++) {
        if (i) await page.waitForTimeout(250);
        const png = await snap(page, { path: `${stem}-motion-${i}.png` });
        if (prev && !png.equals(prev)) moved++;
        prev = png;
      }
      if (moved) notes.push(`${where}: moves (${moved} of ${MOTION_FRAMES - 1} intervals changed): ` +
                            `${path.basename(stem)}-motion-0…${MOTION_FRAMES - 1}.png`);
    },
  },
};
for (const [name, p] of Object.entries(PROFILES)) p.name = name;
let stopFrames = false;

async function frames(browser) {  // the start page at each width × theme, then once under reduced motion
  const dir = path.join(run.out, "frames"), view = slug(new URL(run.url).pathname), junk = new Set();
  fs.mkdirSync(dir, { recursive: true });
  // review: the app's own clock (no frozen time here: that's the frozen profile), and the whole page up to FRAME_MAX_H
  // each way, overflow included, so a sideways spill shows in the frame
  const shoot = async ([width, height], colorScheme, reducedMotion, fn) => {
    const ctx = await browser.newContext({ viewport: { width, height }, colorScheme, reducedMotion, ignoreHTTPSErrors: true });
    try {
      const page = await ctx.newPage();
      await page.goto(run.url, { waitUntil: "load", timeout: 30000 });
      await page.evaluate(() => document.fonts.ready.then(() => 0));
      const [wide = 0, tall = 0, text = ""] = await page.evaluate(() => [document.documentElement.scrollWidth,
        document.documentElement.scrollHeight, document.body ? document.body.innerText : ""]);
      const m = String(text).match(JUNK);
      if (m) junk.add(m[0]);
      await fn(page, wide, { fullPage: true, caret: "hide", clip: { x: 0, y: 0,
        width: Math.min(Math.max(width, wide), FRAME_MAX_H), height: Math.min(Math.max(height, tall), FRAME_MAX_H) } });
    } finally { ctx.close().catch(() => {}); }  // not awaited: a frozen renderer may never answer
  };
  try {
    for (const size of SIZES) for (const theme of THEMES) {
      if (stopFrames) return;
      await shoot(size, theme, "no-preference", async (page, wide, full) => {
        await snap(page, { ...full, path: path.join(dir, `${view}-${size[0]}-${theme}.png`), animations: "disabled" });
        if (wide > size[0] + 1) frameFinding(`frame ${size[0]} ${theme}`, `page wider than the screen (${wide} px > ${size[0]} px)`);
      });
    }
    // reduced motion: once loaded, two frames a second apart are the same picture (no animations: "disabled" here:
    // the point is motion the app itself fails to stop). The pair is the first screen, taken after the full-page
    // frame and a second more, so lazy images the tall capture woke have landed
    await shoot(SIZES[0], "light", "reduce", async (page, wide, full) => {
      await page.waitForTimeout(1000);
      await snap(page, { ...full, path: path.join(dir, `${view}-${SIZES[0][0]}-reduce.png`) });
      await page.waitForTimeout(1000);
      const a = await snap(page, { caret: "hide" });
      await page.waitForTimeout(1000);
      if (!a.equals(await snap(page, { caret: "hide" })))
        frameFinding(`frame ${SIZES[0][0]} reduce`, "still moving under reduced motion (two frames a second apart differ)");
    });
  } catch (e) {
    notes.push(`frame matrix stopped: ${e.message.split("\n")[0]}`);
  }
  if (junk.size) notes.push(`frames: the page shows ${[...junk].map(j => `"${j}"`).join(", ")} (junk text, unless the product means it)`);
}

async function main() {
  const { chromium } = require(process.argv[2]);
  [run.url, run.out, run.profile = ""] = process.argv.slice(3);
  const prof = PROFILES[run.profile];
  if (run.profile && !prof) throw new Error(`unknown profile ${run.profile}`);
  const p = prof || {};
  const finish = () => {
    if (p.end) p.end();
    console.log(JSON.stringify({ views, defects, notes, frame_findings: framed,
                                 ...(motionSamples.length ? { motion: motionSamples.slice(0, 500) } : {}),
                                 ...(motionNotes.length ? { motion_notes: motionNotes.slice(0, 20) } : {}) }));
    process.exit(0);
  };
  // T-0420: a frozen page leaves Playwright calls that never return; whatever happens, print what was found
  setTimeout(() => { notes.push(`stopped at the time limit after ${views.length} views`); finish(); }, DEADLINE + 15000 - Date.now());
  process.on("SIGTERM", () => process.exit(143));  // fm smoke's own limit: exiting runs Playwright's browser kill
  let browser;
  try {
    browser = await chromium.launch();
  } catch (e) {  // an optional dependency, never installed from here: say what's missing and stop
    if (!/Executable doesn't exist|playwright install/i.test(e.message)) throw e;
    console.log(JSON.stringify({ skipped: `no browser for this Playwright: ${e.message.split("\n")[0]}` }));
    process.exit(0);
  }
  if (!prof) await withTimeout(frames(browser), FRAMES_MS).catch(() => {
    stopFrames = true;
    notes.push(`the frame matrix stopped at its ${FRAMES_MS / 1000} s limit`);
  });
  const settle = p.settleMs || SETTLE_MS;
  for (const [label, viewport] of [["desktop", { width: 1440, height: 900 }], ["phone", { width: 390, height: 844 }]]) {
    let where = `${label} start`, ctx;
    try { await withTimeout((async () => {  // a viewport gets its views' share of the deadline, then is abandoned
    ctx = await browser.newContext({ viewport, ignoreHTTPSErrors: true });
    const page = await ctx.newPage();
    page.on("pageerror", e => add(where, `page error: ${e.message}`));
    page.on("console", m => {
      if (m.type() === "error" && !p.quiet && !m.text().startsWith("Failed to load resource")) add(where, `console error: ${m.text()}`);
    });
    page.on("response", r => {  // 4xx from the app's own host (any port), 5xx from anywhere
      const u = new URL(r.url());
      if ((r.status() >= 500 || (r.status() >= 400 && ours(r.url()))) && u.pathname !== "/favicon.ico")
        add(where, `HTTP ${r.status()} ${ours(r.url()) ? u.pathname : u.origin + u.pathname}`);
    });
    page.on("requestfailed", r => {
      const err = (r.failure() || {}).errorText || "";
      if (!p.quiet && ours(r.url()) && !err.includes("ERR_ABORTED")) add(where, `request failed: ${new URL(r.url()).pathname} ${err}`);
    });
    if (p.setup) await p.setup(ctx, page);
    const t0 = Date.now();
    try {
      await page.goto(run.url, { waitUntil: "load", timeout: p.loadMs || 30000 });
    } catch (e) {
      add(where, `did not load (is the server running?): ${e.message.split("\n")[0]}`);
      return;
    }
    if (p.loaded) await p.loaded(ctx, page, label, Date.now() - t0);
    const check = async () => {
      views.push(where);
      let stuck = [];
      for (let t = 0; t <= settle; t += 500) {  // placeholders get the settle time to resolve
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
      for (const s of new Set(stuck)) add(where, `loading placeholder still showing after ${settle / 1000} s (${s})`);
      const stem = shotStem(where);
      if (p.view) await p.view(page, where, stem);
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
      for (const f of found) p.quiet && f.startsWith("alert shown:") ? notes.push(`${where}: ${f}`) : add(where, f);
      await snap(page, { path: stem + ".png" });
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
          await page.goto(href, { waitUntil: "load", timeout: p.loadMs || 30000 });
        } catch (e) {
          if (p.quiet) notes.push(`${where}: did not load offline (${e.message.split("\n")[0]})`);
          else add(where, `did not load: ${e.message.split("\n")[0]}`);
          continue;
        }
        await withTimeout(check(), VIEW_MS);
      }
    }
    })(), Math.max(VIEW_MS, (DEADLINE - Date.now()) / (label === "desktop" ? 2 : 1))); } catch (e) {
      if (e === HUNG) outOfTime(p, where);
      else add(where, `crawl error: ${e.message}`);
    }
    if (ctx) ctx.close().catch(() => {});  // not awaited: a frozen renderer may never answer
    if (Date.now() > DEADLINE) { notes.push(`stopped at the time limit after ${views.length} views`); break; }
  }
  await withTimeout(browser.close(), 10000).catch(() => {});
  finish();
}

module.exports = { PROFILES, SIZES, THEMES, FRAME_MAX_H, frames, outOfTime, slug, run, sampleMotion,
                   state: { views, defects, notes, frame_findings: framed } };
if (require.main === module) {
  main().catch(e => {
    add("smoke", `crawl crashed: ${e.message}`);
    console.log(JSON.stringify({ views, defects, notes, frame_findings: framed }));
    process.exit(0);
  });
}
