## Verdict
Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did not run the build or render a page, so the findings marked "unrendered" below rest on reading the CSS and code only.

## lens: adversary
- MEDIUM — ~/.claude/foreman/site/pages.py:115 — `<td>{c['case']}</td>` is the only unescaped data value. `case` comes from `stats.py name()`, which takes the first five words of a task title from `cases.json`. A title such as `<script>alert`1`</script>` reaches the page as live HTML, and a title with `&` produces invalid HTML. Everywhere else `esc()` is used. — Use `{esc(c['case'])}`. — high
- MEDIUM — ~/.claude/foreman/site/build.py:260 — `build()` runs `shutil.rmtree(out)` on whatever path argv gives it. `python3 site/build.py .` from the repo root deletes the repo including `.git`. `python3 site/build.py ~` deletes the home folder. — Refuse when `out` equals or contains `ROOT` or `HERE`, or only wipe a directory that is empty or holds a marker file. — high
- LOW — ~/.claude/foreman/.github/workflows/pages.yml:11 — One job runs repo Python while holding `pages: write` and `id-token: [REDACTED], and actions are pinned by tag. — Split into a build job (contents: read) and a deploy job, and pin actions by SHA. — medium

## lens: edge
- LOW — ~/.claude/foreman/site/build.py:155 — `line()` with `rows == []` raises IndexError at `xs[-1]`. This happens when `releases()` finds no release commits. With 2 rows, the label loop at 156 draws the last label twice. — Return a "no data" note when `rows` is empty and use `sorted({0, n//2, n-1})`. — high
- LOW — ~/.claude/foreman/site/stats.py:134 — `bench()` writes `{}` if bench_hooks prints nothing or fails. The Speed, Guard and Panel charts then render a blank 8px SVG with no message. — Exit nonzero when `data` is empty, and have `hbars` show a "no data" figure for zero items. — medium
- LOW — ~/.claude/foreman/site/stats.py:195 — `--duel long=DIR` alone replaces every saved duel. `old.get("duels")` is used only when the new list is empty, so quality, hard and hard-haiku revert to "Not run yet". — Merge the new duels over the old ones by name. — high

## lens: intent
- MEDIUM — ~/.claude/foreman/site/style.css:227 — The line chart's `<polyline class="ln s1" fill="none">` is hit by `.viz .s1 { fill: var(--s1) }` at line 229. A CSS rule beats the presentation attribute, so the polyline is filled with a wedge between the curve and its chord. This affects the Learning and Releases pages. Unrendered. — Add `.viz .ln { fill: none; }` after line 229, or style `.viz polyline.ln`. — medium
- LOW — ~/.claude/foreman/site/style.css:222 — Only `.pairs` text gets a larger size on phones. The hbars, columns and line charts scale a 640px viewBox down to about 330px, so 12.5px text renders near 6.5px. There is no horizontal scroll, but the labels are hard to read. — Apply the same bump to `.viz` text under 560px. — medium

## lens: operator
No separate finding. The `rmtree` risk (build.py:260) and the stats.py failure modes under edge apply here too.

## lens: maintainer
- LOW — ~/.claude/foreman/site/pages.py:339 — Prose hard-codes figures (24 and 20 and 4 and 25, "10%/29% more", "Both sides passed everything") that the charts below it compute from data. The Foreman Code page also hard-codes 52 and 9 (pages.py:332). The test only checks the text "24 dangerous", so these drift silently. — Build the figures from `s["safety"]` and `s["duels"]`, or pin them in a test. — high
- LOW — ~/.claude/foreman/site/stats.py:5 — The docstring says "never a task title", but duel `case` names come from titles and `found` holds `(discovered)` titles. `build.py:262` copies `data/stats.json` into the published site. — Correct the docstring, or leave `data/` out of the copy. — high
- LOW — ~/.claude/foreman/site/build.py:22 — The `fmt` condition mixes `and` and `or` without parentheses. Other leftovers: `pairs` has a constant `label_w = 0`, `tiles(pairs, …)` shadows the `pairs` function, `verdicts` has an unused `allow` stamp key, and `stats.ledger(state, kinds)` has an unused `kinds` argument. — Parenthesise `fmt` and delete the leftovers. — high

## Acceptance criteria
- **Every feature page builds with a chart or tiles, nav and footer:** met. The test asserts the chart classes and `class="side"`, and `layout()` always emits the nav and footer.
- **No broken local links:** met. The test checks every src, href and poster, plus in-page anchors.
- **Light and dark themes:** met in CSS, with tokens for both. Not tested. The polyline fill above is a dark and light bug alike.
- **Phone width without horizontal scroll:** not verifiable from the code. `body{overflow-x:hidden}` hides any overflow. Chart text is small (see the intent lens).
- **The workflow runs `python3 site/build.py _site` and deploys:** met.

## Implicit decisions
- The build copies all of `site/` except a short list of source files, so the data JSON is published.
- `bench.json` is merged over `stats.json` by key.
- Hand-rolled SVG on a 640-wide viewBox, with a text-width estimate of about 6.5px per character.
- `dangerous` rows always show "Runs" for Claude Code.
- A duel with no cases shows "Not run yet".

## Not checked
- Rendering in a browser.
- The landing page `site/index.html`.
- `bench_safety.py` beyond its header.

**Noticed:** `site.js` and `style.css` apply the stored theme only after the page loads (the script sits at the end of body), so a stored "light" choice on a dark OS flashes dark first.
