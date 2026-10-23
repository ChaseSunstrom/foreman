<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Visual QA: screenshots, an eyeball pass and a receipt

Use when a task changes what a web screen looks like: a new view, a restyle, a dark mode, a layout fix, a motion change. Green tests say the code does what the tests ask; only a frame says the screen looks right. This playbook proves a UI change by looking at it: `fm smoke` for the defects a crawler can name, the start page's frames and hostile profiles, a small frame script for the other views and fixtures, a checklist for the eye, and a receipt in the task's evidence.

It checks the decisions the sibling playbooks make; it doesn't repeat them. The stance and the cover test are in `design-direction.md`, the scale, palette and contrast proof in `type-and-colour.md`, the reduced forms in `motion.md`, a WebGL scene's survival probes in `scene-3d.md`. Terminals: `terminal-ui.md`.

## The two passes

| Pass | What runs | Widths | Themes, motion | Finds |
|---|---|---|---|---|
| `fm smoke` | Foreman's crawler (`smoke_web.cjs`) in a headless Chromium | crawl: 1440×900, 390×844; the start page's frames: 360×800, 768×1024, 1440×900 | crawl: the browser's defaults; frames: light and dark, reduced motion at 360 | load and console errors, failed requests to the app's host, placeholders still showing after 5 s, visible alerts, a page wider than the screen, overlapping fixed controls; from the frames, as notes: overflow, motion under reduce |
| frame script | `qa/frames.mjs` below, in the project | 360×800, 768×1024, 1440×900 | light and dark; reduced motion at 360 | the same frames for every path you name, on a seeded fixture: page overflow, junk text, a screen that still moves under reduced motion; and the frames the eye checks |

Both use the project's own Playwright; Foreman never installs it. Without it, or with it but no browser, `fm smoke` prints `skipped …` and the reason, which is not a pass: `npm i -D playwright`, then `npx playwright install chromium` (or point `FOREMAN_PLAYWRIGHT` at a Playwright package folder).

## fm smoke

1. Start the app on the seeded fixture (next section), then record its address once per project: `fm smoke set web http://localhost:5173`. This also adds `fm smoke` to the project's gates, so `fm check` runs it from then on.
2. Run it: `fm smoke` (same as `fm smoke run`). It first shoots the start page's frame matrix (the frame script's, each frame at most 8000 px each way), then opens the page at desktop and phone width, clicks each visible tab among the first 24 `role="tab"` elements (with none, follows up to 10 same-origin nav links), and checks each view. Exit 0 means no defects; each defect prints as `✗ <viewport> <view>: <what>`. The frames' findings are notes (`· frame 360 reduce: still moving …`), so a live page keeps its gate; `--strict` (or `fm smoke set strict on`) fails on them too.
3. The last lines are `Screenshots: <dir>`, a PNG per view named after it (`desktop-start.png`), and `Frames: <dir>/frames`, named as the frame script names them (`home-360-light.png` … `home-360-reduce.png`). The folder is `<project state>/smoke/<commit>/default` (`<commit>-dirty-<diff hash>` with uncommitted changes); a re-run on the same tree replaces it and five such folders are kept, so a receipt for the start page can point at its frames.
4. A UI no URL serves (a plugin's own panel, an Electron shell): `fm smoke set off <why>` stops the gate. The frame script and the eyeball pass still apply wherever a page can be opened.

### Hostile profiles

`fm smoke --profile NAME` (repeatable, or `all`) crawls the same views under one hostile condition instead, into `<commit>/<profile>/`. Not a gate, and exit 0 on findings unless strict: run them when a task touches layout, data loading or colour, and fix or `fm capture` each finding. A profile can take four minutes, so in Claude Code run `--profile all` in the background (Bash's `run_in_background`).

| Profile | What it does to the page | What it finds |
|---|---|---|
| `torture` | 90-letter words, right-to-left runs, 20-digit numbers in the page's text | text out of its box, a page wider than the screen |
| `empty` | every list in the app's own JSON emptied | a crash with no data; its empty states |
| `offline` | network cut after the first load | uncaught errors, endless spinners |
| `slow3g` | 2 s latency, 50 KB/s | load time (a note), placeholders past 15 s |
| `deuteranopia`, `protanopia`, `tritanopia`, `achromatopsia` | a colour-vision filter | frames for the eye: a state told by colour alone |
| `frozen` | clock fixed, animations paused | a view that still changes (a note) |
| `motion` | five frames 250 ms apart per view | which views move (a note) |

Open the PNGs with the Read tool as in "Looking at the frames".

Pass: `fm smoke` exits 0 on the commit you're reporting, and its output says how many views it saw. One view where you expected several means its tabs aren't `role="tab"` or its nav isn't in `nav` or `role="navigation"`: fix the markup, not the crawler.

## Seeded fixture

A frame is evidence only if the next run on the same commit draws the same pixels. Everything that changes between runs is a moving part to remove, not to mask.

1. **Data comes from a seed, not from whatever the dev database holds.** One command or variable puts the app on it (`QA_FIXTURE=full npm run dev`, a seed script, a mock server). Two fixtures at least: `full` and `empty`.
2. **`full` holds the hard cases on purpose:** the longest real name you'd accept (60 characters or more, no spaces in one of them), a 7-digit amount, a missing avatar, a negative number, a right-to-left word if the product takes user text, and enough rows to scroll (finite: about 50, not an infinite feed).
3. **`empty` is a brand-new account:** every list, table and chart with nothing in it. What each empty, loading, error and overflow state should look like is `composition.md`'s state atlas; this pass checks the built screens against it.
4. **Time is frozen** at the fixture's "now" (`page.clock.setFixedTime` in the script); relative dates ("3 days ago") are seeded relative to it.
5. **No randomness and no third parties:** seeded IDs and colours, no live ads, maps, embeds or analytics in the QA build, fonts served locally.
6. **Fonts load before capture** (`document.fonts.ready`); a frame in the fallback font is a different screen.

Pass: run the frame script twice on one commit and fixture; every hash it prints matches. A hash that differs names the frame with the moving part.

## Frame script

`fm smoke` already shoots this matrix for the start page on whatever data the running app has; the script covers every other path, on a seeded fixture. Copy it into the project as `qa/frames.mjs` and add `.qa/` to `.gitignore`. It writes the frames to `.qa/frames/<commit>-<fixture>/` (a `-dirty` commit when the tree has changes), prints a short hash per frame, checks what a script can, and exits 1 on any finding. `QA_FIXTURE` only names the folder: the app must already be running on that fixture, so start both with the same value.

```js
// qa/frames.mjs: the frame matrix of Foreman's visual QA playbook (ui/visual-qa.md).
// QA_FIXTURE=full node qa/frames.mjs http://localhost:5173 / /settings /projects
import { chromium } from "playwright";
import { createHash } from "node:crypto";
import { mkdirSync } from "node:fs";
import { execSync } from "node:child_process";

const [base, ...paths] = process.argv.slice(2);
if (!/^https?:\/\//.test(base || "") || !paths.length) {
  console.error("usage: QA_FIXTURE=<name> node qa/frames.mjs <http(s) base url> <path>...");
  process.exit(2);
}
const rev = execSync("git describe --always --dirty").toString().trim();
const out = `.qa/frames/${rev}-${(process.env.QA_FIXTURE || "full").replace(/[^\w-]/g, "")}`;
mkdirSync(out, { recursive: true });
const SIZES = [[360, 800], [768, 1024], [1440, 900]];
const NOW = new Date("2026-01-15T10:00:00Z");  // the fixture's "now"
const JUNK = /\bundefined\b|\bNaN\b|\bnull\b|Invalid Date|\[object Object\]|lorem ipsum/i;
const slug = p => p.replace(/[^\w]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "home";
const hash = png => createHash("sha256").update(png).digest("hex").slice(0, 12);
const bad = [];
const browser = await chromium.launch();

async function open(path, [width, height], colorScheme, reducedMotion) {
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme, reducedMotion });
  const page = await ctx.newPage();
  await page.clock.setFixedTime(NOW);
  await page.goto(new URL(path, base).href, { waitUntil: "load", timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  return { ctx, page };
}

for (const path of paths) {
  for (const size of SIZES) for (const theme of ["light", "dark"]) {
    const { ctx, page } = await open(path, size, theme, "no-preference");
    const file = `${out}/${slug(path)}-${size[0]}-${theme}.png`;
    const png = await page.screenshot({ path: file, fullPage: true, animations: "disabled", caret: "hide" });
    const wide = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    if (wide > 1) bad.push(`${file}: ${wide} px wider than the screen`);
    const junk = (await page.innerText("body")).match(JUNK);
    if (junk) bad.push(`${file}: shows "${junk[0]}"`);
    console.log(`${hash(png)}  ${file}`);
    await ctx.close();
  }
  // reduced motion: once loaded, two frames a second apart are the same picture
  const { ctx, page } = await open(path, SIZES[0], "light", "reduce");
  await page.waitForTimeout(1000);
  const a = await page.screenshot({ path: `${out}/${slug(path)}-360-reduce.png`, fullPage: true, caret: "hide" });
  await page.waitForTimeout(1000);
  const still = a.equals(await page.screenshot({ fullPage: true, caret: "hide" }));
  if (!still) bad.push(`${slug(path)}: still moving under reduced motion`);
  console.log(`${hash(a)}  ${out}/${slug(path)}-360-reduce.png  reduce-still ${still ? "ok" : "MOVING"}`);
  await ctx.close();
}
await browser.close();
for (const b of bad) console.log(`✗ ${b}`);
console.log(`${bad.length ? "✗" : "ok"} ${paths.length * 7} frames in ${out}`);
process.exit(bad.length ? 1 : 0);
```

Why these widths: 360 is the narrowest phone in common use (the smallest width a layout must survive), 768 is a tablet held upright and the usual seam between a phone layout and a desktop one, 1440 is a laptop. `fm smoke`'s 390 sits between the first two; it doesn't replace either. The reduced-motion frame is taken without `animations: "disabled"` on purpose: the point is to catch motion the app itself fails to stop (autoplay video, a canvas loop, a carousel timer).

It ignores a `null` that the product shows on purpose (a database tool): drop `null` from `JUNK` there and say so in the receipt.

## Looking at the frames

The eye is the check here; the script only finds what it can name. Look at every frame of every view the task changed: seven per view per fixture. Views the task didn't touch need only `fm smoke`.

- **In a Claude Code session** (Foreman's plugin): run `fm smoke` and the frame script with Bash, then open each PNG the script printed with the Read tool, which shows the image. Look at them one view at a time, the six themed frames and then the reduce frame, and write the receipt from what you saw. A frame you didn't open is a frame you didn't check: list only those you read.
- **In `fm code`:** its model reads text, not images. Name the frame script in the request as a criterion's verify ("done when the frames are clean :: QA_FIXTURE=full node qa/frames.mjs http://localhost:5173 / /settings") so the plan carries it and the harness records its run; `--verify "<that command>"` fits only a fix the script already fails on (an overflow, junk text), since `--verify` must fail before the change. Leave the eyeball line of the receipt as `eyeball: pending`. The look then happens in a Claude Code session or by a person, from the frame folder the evidence names; a finding becomes a fix task (`fm capture`).
- **By hand:** open the frame folder in an image viewer at 100% zoom, never scaled to fit (a 1 px overlap disappears when shrunk).

## Eyeball checklist

Each line passes only if it holds on every frame you looked at. A failure is fixed and the frames retaken, or captured as its own task and named under `found:` in the receipt; it is never left out.

**Overlap**
- [ ] No text sits on other text, an icon or an image edge; no control covers part of another.
- [ ] Badges, counters and avatars stay inside the thing they belong to, including with the fixture's 7-digit amount.

**Overflow**
- [ ] Nothing is cut at a frame's right edge and no panel, table or card shows a scrollbar it didn't need (the script catches only the whole page).
- [ ] The fixture's longest name fits, wraps or ends in an ellipsis inside its box; the spaceless one doesn't push its column wider than the screen.
- [ ] At 768, the navigation fits on one row or collapses whole; never a second row holding the last link or two.

**Contrast**
- [ ] Every text and icon reads at arm's length in both themes, including placeholders, disabled controls, chart labels and text over images (the contrast proof in `type-and-colour.md` has the numbers for listed pairs; this catches the unlisted ones).
- [ ] The dark frames have no light patch left over: no white card, input, menu, chart background or image with a white box around it.

**Alignment**
- [ ] Stacked blocks share their left edge; gaps between siblings in one group are equal.
- [ ] Numbers in a column are right-aligned and line up digit for digit; icons sit centred on their text's line.
- [ ] At 1440, content isn't a phone-width column stranded at one side, and running text isn't stretched across the whole screen.

**Empty and odd states** (the `empty` fixture, plus the hard cases in `full`)
- [ ] Every empty list, table and chart says what's missing and offers the one action that fills it; no blank box, lone header row or axis with no data.
- [ ] No raw translation keys (`nav.settings.title`), template braces or placeholder copy anywhere (the script finds `undefined`, `NaN`, `null`, `Invalid Date`, `[object Object]` and lorem ipsum; keys and braces need the eye).
- [ ] A missing avatar or image shows a designed fallback, not a broken-image icon or alt text spilling out.

**Reach**
- [ ] At 360, the primary action is on the first screen or one scroll away and is about a fingertip high (44 px or more in the browser's devtools).

**Motion**
- [ ] Every `reduce-still` line says `ok`, and each reduce frame shows the same settled screen as its light frame at 360: nothing half-faded, off-screen or mid-slide (the reduced forms themselves are in `motion.md`).

**Direction**
- [ ] The cover test from `design-direction.md` passes on the main view's 1440 light frame.

## Receipt

The receipt goes in the task's evidence, so the close shows what was looked at and when. Three records, in order:

1. `fm task evidence <ID> --step N --run "fm smoke"`: the crawl, with its real exit code.
2. `fm task evidence <ID> --step N --run "QA_FIXTURE=full node qa/frames.mjs <url> <path>..."`, and the same for `empty`: the frame paths, their hashes and the script's checks.
3. The look, typed because it can't be run:
   `fm task evidence <ID> --step N "eyeball <frames folder>" "<the receipt line below>"`

The typed line, one per fixture:

```
eyeball .qa/frames/<commit>-<fixture>: <views> × 360/768/1440 × light/dark + reduce, <n> frames read
overlap ✓ overflow ✓ contrast ✓ alignment ✓ empty ✓ reach ✓ motion ✓ direction ✓
found: <frame file>: <what> → fixed in <commit> | captured T-NNNN | none
```

Example:

```
eyeball .qa/frames/a41c9e2-full: home, settings, projects × 360/768/1440 × light/dark + reduce, 21 frames read
overlap ✓ overflow ✗ contrast ✓ alignment ✓ empty ✓ reach ✓ motion ✓ direction ✓
found: projects-768-dark.png: owner column pushed past the edge by the spaceless name → fixed in b07d311, retaken
```

Rules:
- The commit in the folder name is the one being reported (the latest fix included), never `-dirty`; retake after the last change.
- Each mark is ✓ or ✗, never left blank; a ✗ has its `found:` line, and every `found:` ends in a fix commit or a task id.
- `<n> frames read` counts the frames actually opened; under the frame count means the receipt says which views weren't looked at.
- From `fm code`, the line is `eyeball .qa/frames/<commit>-<fixture>: pending` until someone looks.

## Going further

This is a look per task, not a regression suite. When a screen stops changing, turn its frames into committed baselines with `toHaveScreenshot` (`fm lib show visual-regression`), so a later task that moves a pixel fails a test instead of waiting for an eye.

## Checks

- [ ] `fm smoke` exits 0 on the reported commit, with more than one view per width when the app has tabs or nav.
- [ ] The frame script exits 0 for `full` and `empty` on the reported commit, and a second run prints the same hashes.
- [ ] `.qa/` is in `.gitignore`; no frame is committed.
- [ ] Every line of the eyeball checklist is marked in the receipt for every view the task changed.
- [ ] The task's evidence has the three records above, and every `found:` ends in a fix commit or a task id.

## Library cards

The tooling lives in the stack library: `fm lib show playwright` (contexts, locators, emulation), `fm lib show visual-regression` (committed baselines, masking, pinned rendering), `fm lib show test-fixtures` (scoped seeds with clean-up), `fm lib show dark-mode` (the theme switch the dark frames exercise), `fm lib show animation` (reduced motion in code), `fm lib show responsive-design` (breakpoints the 768 frame tests), `fm lib show accessibility-testing` (what an automated scan adds to the eye), `fm lib show e2e-strategy` (which journeys deserve a test of their own).

## UI contract

- motion: reduced motion is its own column in the frame matrix.
- contrast: the receipt records a contrast check per frame, not only how it looks.
- keyboard: a focus-visible frame (Tab pressed once) is part of the matrix.
- small screens: 360 px is the matrix's first width, and any sideways scroll fails the frame.
- states: the seeded frames include empty, loading, error and done for each screen.
