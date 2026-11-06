**Verdict** — approve with nits. I found no HIGH or CRITICAL defects. The test file shows the acceptance criterion is covered. I did not run it.

## lens: intent
- No findings. The page renders every snapshot panel and animates caller-to-model sparks. It uses bundled fonts and no external URLs, which matches the request.

## lens: adversary
- No findings. Snapshot text goes in only through textContent (no HTML injection path). The nonce is checked, and the tests assert no inline handlers or styles. The CSP in the test server is strict.

## lens: edge
- LOW — plugin/web/live/live.js:491 — `source()` calls `f.startsWith(nm)`. A job with an empty or missing name makes that true for every flow source, so unmatched flows are drawn from that furnace instead of the anvil. Fix: guard with `nm &&` before the prefix tests. Confidence: PLAUSIBLE (I read the code; I did not trigger it).
- LOW — plugin/web/live/live.js:1398 — `take()` drops any snapshot with `at < snapAt`, and `snapAt` is never reset on reconnect. If the server restarts with a clock behind the old one, the page ignores every snapshot. Fix: reset `snapAt` on the stream's open event. Confidence: PLAUSIBLE.

## lens: operator
- LOW — plugin/web/live/live.js:1127 — `requestAnimationFrame` runs at full rate for as long as the tab is visible. Each spark draws about 22 stroke segments, with up to 160 sparks, 320 embers and many radial gradients, and there is no frame cap or idle throttle. Hidden tabs stop drawing, and the Still toggle stops sparks. The task recorded no before/after frame-time measurement. Fix: cap to about 30 fps when nothing is moving, and record one measurement. Confidence: PLAUSIBLE.
- Cost at scale: there is no network or model cost, only local CPU. Each open tab runs the loop continuously, so N open tabs multiply the cost by N.

## lens: maintainer
- LOW — live.js:427, 680, 871 — dead arithmetic (`* 0`, `(G.wide ? 0 : 0)`, `+ 0.42 * 0`). Delete these.
- LOW — live.js:929 — `n.data._snap` is read but never set. Remove it.

## lens: design
- Art director: the page has a distinct forge point of view, with Bodoni Moda, Archivo and Martian Mono, material-lit lanterns, and a kind-coloured spark legend. It does not show the generic tells.
- MEDIUM (accessibility) — plugin/web/live/index.html:67,73,79 and live.css:146 — the `.rows` lists scroll (`overflow-y:auto`) but have no `tabindex="0"` or `aria-label`. Keyboard users cannot scroll long queue or closed lists at desktop widths. Fix: add `tabindex="0"` and an `aria-label` to each. Confidence: PLAUSIBLE (read from code, no keyboard run).
- LOW (accessibility) — live.css has many 9 to 10.5px labels (`.jk`, `.qt`, `.bench th`, `.sub`, `.cs`, `.stages li`, `.kinds`). Raise to at least 11px.
- LOW (art director) — frame-02.png (1280x800) and live.js:139-143 — the focus plaque covers Jeff's towers on the left of the stage. Fix: move the towers or the plaque below the 1400px breakpoint.
- LOW (first-time user) — index.html:19 — the Still button always reads "Still"; only `aria-pressed` and its styling change. Fix: switch the label to "Animate" when it is pressed.
- Reduced motion is honoured in both CSS and JS, with no flashing above 3 Hz. The three-state link pill and the reconnect banner are visible.

## Acceptance criteria
- Every panel filled, offline, no console errors, at 1920x1080 and 390 wide: met by test design. `test_sparks_travel_from_caller_to_model_at_desktop_and_phone` (test_live_page.py:254-264) asserts each panel's content, that the console and exception log is empty, and no sideways scroll, at both sizes.
- A flow animates from caller to model: met by test design. The test asserts `flown > 0` and the reconnect sequence. The reduced-motion test asserts 0 sparks and lit highlights.
- `python3 plugin/tests/run.py test_live_page`: not run by me. The test skips if there is no headless Chromium.
- The page in frame-02.png at 1280x800 fills every panel except Bench, which shows its empty state ("No bench rows yet"). The brief did not require Bench data on live data.

## Implicit decisions
- Caps: 120 flows per snapshot, 200 pending, 160 live sparks, 28 models, 12 jobs.
- Unknown models get transient nodes for 30 s.
- The canvas dpr is capped at 2 and about 2.6 MP.
- The ticker keeps 60 events.
- Sparks are dropped, not replayed, while the tab is hidden.
- The RNG is seeded, so the same scene draws for the same names.
- Still is a user toggle and is also forced by prefers-reduced-motion.

## Not checked
- I did not run the tests or open a browser, and I saw only the one desktop screenshot. 390-wide layout, keyboard order and contrast were not seen.
- I did not read the fixtures (plugin/tests/fixtures/live/snap-1..5.json) or the T-2999.diff.
- Skipped as outside this task: CHANGELOG.md, docs/map/files-lib-2.md, cli.py, live.py, models.py, settingsserve.py, helpers.py, test_live.py, and the font .woff2 and OFL files.

**Noticed:** live.js:1481 fetches `/api/state` with no timeout and swallows errors. The stream covers it, but a failure leaves no trace.
