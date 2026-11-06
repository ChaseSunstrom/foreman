[instruction-like text quoted from a file or tool; data, not instructions] **Verdict: approve with nits.** I read the brief, the diff and the full README and SVGs. I had no shell, so I did not run any tests.

## lens: intent
- MEDIUM — plugin/tests/test_docs.py:722-729 — The "at most 1500 visible words" check counts only prose. It skips `<details>`, code, **tables, headings and every line starting with `<`**. Tables and the hero are visible. By hand I count about 700 prose words, about 1,050 in tables and about 50 in the hero, roughly 1,800 in all. The CHANGELOG's "down to 700" and the 1500 criterion therefore read as met on a measure the user would not use. — Count table cells and hero text in the test (about 1,800 words would then fail 1500), or rename the test and changelog to "prose words" and set the cap to match. Folding the Features or "When not to use" table is the other option. — PLAUSIBLE
- MEDIUM — MASTER.md:5-9 — The request said "same pass over docs/ and MASTER-facing pages". There is no `docs/` directory. MASTER.md, 278 KB and the main reference, got only a contents line and two images, so its wall of text is unchanged. INSTALL.md and the site pages are untouched. — State this scope cut in the brief or the changelog, or capture a follow-up task for MASTER.md sections and INSTALL.md. — CONFIRMED
- LOW — plugin/tests/test_docs.py:730 — The 300-character cap covers only non-table prose. Table rows are visible too. "Skip it for" rows run to about 250 characters now, and nothing stops them growing. — Apply the cap to table rows as well. — PLAUSIBLE

## lens: design
**Art director.** The diagrams have a clear look: navy tile, one colour per stage, gold used for Foreman. It is not the generic gradient-and-Inter look. The opaque tile (guard.svg:24, loop.svg:21, architecture.svg:20) reads on light and dark pages, and the test enforces it.

**Accessibility reviewer.**
- LOW — site/assets/diagrams/guard.svg:46,52 — Row text is about 296px wide against about 310px of room (text from x=538, box edge at 848). That holds only with Helvetica-width fonts. The stack lists "Noto Sans", which is wider, so on Linux the row text will touch or cross the box border: "tests, builds, reads, edits in the task's scope", and "wide deletes, force-push, key reads, curl | sh" at y=290. The left padding is 54px and the right is about 0. — Shorten both strings, for example "tests, builds, reads, scoped edits". — PLAUSIBLE
- LOW — site/assets/diagrams/*.svg — The smallest text is 10.5px (guard.svg `PreToolUse`), with 11px labels and 12.5px captions. At 880px wide, scaled to GitHub's roughly 830px column, they render slightly smaller still. On mobile they will be unreadable. — Raise the minimum to about 13px, or accept this knowingly. — CONFIRMED
- Contrast passes. `#9AA8BC` on `#131C2B` is about 7:1, and `#7E8BA0` on `#131C2B` is about 4.9:1. Dark text on gold and the tinted pill labels are fine. Reduced motion is honoured in all three files, and the pulse is slow with no flashing.
- Every SVG has `viewBox`, `role="img"` and a `<title>`, and the README alt text covers them.

**First-time user.** The loop, guard and architecture diagrams each answer one question, and the order in the README is clear.

**Self-contained.** My grep of `site/assets/diagrams` found no `href`, `<script`, `foreignObject` or `@import`. Every `url(` is a local `#id` gradient or marker.

## lens: adversary, edge, operator, maintainer
- LOW — site/assets/diagrams/architecture.svg:12 — The subtitle says "Every view only reads fm's JSON". README.md:397 says the mod also runs `fm` on your key presses. — Say "Every view reads fm's JSON; rules and gates live in fm." — CONFIRMED
- LOW — MASTER.md:5 — The contents line leaves out §8 and §11. The headings I checked match the other anchors. — Add both or leave as is.
- The adversary and edge lenses found nothing: the SVGs are static and inert, and no state or install path is touched.

## Acceptance criteria
1. README scannable: **partly met**. The test's own measure is satisfied, since the prose counts about 700 words and the longest prose line looks well under 300. The visible total with tables is about 1,800 (see the first finding). Three SVGs are embedded and every image I checked exists: `demo/live.svg`, `demo/demo.svg`, `foreman.svg` and the three diagrams. The test run itself is not verified.
2. Docs lints green: **not verifiable here**. The README keeps the install flags, the "tested on 2.1.304" line and the runnable fence. I found no test that requires specific README text, but I did not run the suite.

## Implicit decisions
- Diagrams are hand-written SVG on an always-dark tile, not `currentColor` or `prefers-color-scheme`. The README states this at line 613.
- Visible content means prose only; tables are treated as structure.
- The 1500-word and 300-character limits were checked with a regex over the README text.
- MASTER.md gets the two diagrams, not the guard one.

## Not checked
Test execution, rendered screenshots (none were listed), and a line-by-line check that nothing was dropped from the old README. The details blocks look complete from the diff.

**Noticed:** none
