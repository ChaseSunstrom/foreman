---
id: T-2061
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T23:29:52Z
updated: 2026-10-29T23:45:29Z
base: 389961bce2816cc6234c690622b6c66f8272d2ee
base_tree: 655a692eb436b6972f50fe21a137d58ebf9e1293
plan0_at: 2026-10-29T23:37:46Z
plan0_scope: []
verified: strong
---
# Site's fm code section is stale; show the current fm code (TUI, verbs, recording) as it…
## Raw request
> FIX: site's fm code section is stale; show the current fm code (TUI, verbs, recording) as it is today
## Interpretation
The fm code page plays code-tui.mp4, recorded Oct 20; ~130 fm code commits since (queue, ask, undo, PR, photo booth, tickets, chaos, why) aren't on the page, and its key list is hand-typed.
## Assumptions (confidence)
## Acceptance criteria
- [x] the built code page shows the tour drawn from current code and every key fm code tui binds, no stale video — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_code_page_is_drawn_from_todays_tui`
## Non-goals
## Approach (options → choice → why)
Options: (a) re-record the mp4 (stales again); (b) build draws the animated tour SVG from current code each build, keys table generated from fmcodetui's own key map (chosen: can't go stale, no committed video); (c) screenshot per view (heavy). Picture element: reduced motion gets the still snapshot. Copy gains a block for the newer verbs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] build draws the tour + keys table; page copy for new verbs; drop code-tui.mp4
3. [x] screenshot review of the built page
## Resume here
<!-- auto -->
- 2026-10-29T23:39:24Z step 1/3: failing test
- git: foreman/build; 3 uncommitted: plugin/tests/test_site_build.py, site/build.py, site/pages.py
- touched since last checkpoint: plugin/tests/test_site_build.py, site/build.py, site/pages.py
## Docs impact
README.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_code_page_is_drawn_from_todays_tui` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Landing 0s) / FAILED (1 classes) [ran] [tree 48852204d5f5] (2026-10-29T23:37:58Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 10 tests in 1.2s (5 classes, 16 at a time; slowest: Landing 1s, Reproducible 1s, TitleCard 0s) / OK [ran] [tree 3fe2e61c23d2] (2026-10-29T23:41:34Z)
- (step 3) `~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --no-sandbox --hide-scrollbars --virtual-time-budget=14000 --window-size=1040,678 --screenshot=/tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/tour14.png file:///tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/sb/assets/code-tui-tour.svg 2>/dev/null && test -s /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/tour14.png` → exit 0 · (no output) [ran] [tree 3fe2e61c23d2] (2026-10-29T23:41:44Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → ✗ exit 1 · Ran 10 tests in 1.6s (5 classes, 16 at a time; slowest: Landing 1s, Reproducible 0s, TitleCard 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ea162eb7316c] (2026-10-29T23:42:00Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 10 tests in 1.2s (5 classes, 16 at a time; slowest: Landing 1s, Reproducible 1s, TitleCard 0s) / OK [ran] [tree ea162eb7316c] (2026-10-29T23:42:00Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 23:20 UTC; claude plugin test mods/foreman-ui → [ran] [tree ea162eb7316c] (2026-10-29T23:45:06Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_code_page_is_drawn_from_todays_tui` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Landing 0s) / OK [ran] [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_code_page_is_drawn_from_todays_tui` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Landing 0s) / OK [ran] [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit intent) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → the code page is now drawn from today's fm code at every build (tour SVG, still under reduced motion), every bound key comes from DEFAULTS['keys'] with its COMMAND_LABELS label, and the newer verbs (queue, ask, follow-ups, undo/PR/hand-off, why, chaos) have a block checked against fm code --help [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit adversary) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → every label, key name and CLI hint goes through esc; nothing user-typed reaches the page [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit edge) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → a bound command with no label shows its command name; one outside POSTER lands in a 'more' group; reduced motion gets the still code-tui.svg via <picture>; two builds stay byte-identical (Reproducible passed) [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit operator) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → the build draws the tour each time (deterministic, about 724 KB, lazy-loaded); the README's demo links point at the site so they can't go stale; demo/code-tui.mp4 and demo/code-tui-tour.svg stay committed but unused (the guard refuses the tree delete) [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit maintainer) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → one _tui loader and one _keys table in pages.py; the test fails when a key is bound without reaching the page [tree ea162eb7316c] (2026-10-29T23:45:19Z)
- (audit design) `self-review of the diff (build.py tour line, pages.py _tui/_keys and the code page blocks, README links, test) plus two screenshot reads` → 1280x3400 shot of features/code.html read: tour in its frame, list block, grouped key table; the tour SVG alone at 14 s shows the guard caption mid-run [tree ea162eb7316c] (2026-10-29T23:45:19Z)
## Log
- 2026-10-29T23:29:52Z created
- 2026-10-29T23:37:45Z planned: it has criteria and steps
- 2026-10-29T23:37:46Z focused
- 2026-10-29T23:45:22Z done
- 2026-10-29T23:45:24Z committed 03b7feea (5 files)
- 2026-10-29T23:45:29Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1546 [FEATURE M, done, 6 steps] Round 3 (T-1520): fm code app visual extras: a photo booth for frames, an isometric layout — lesson: A chaos harness is safe to run any…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
## Why not caught
the site played a recording committed once (code-tui.mp4, Oct 20) and hand-typed keys; nothing tied the page to the TUI's current code
## Lessons
- A page that shows an app should be drawn by the app at build time; a committed recording or hand-typed key list goes stale silently
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_site_build.py
- site/build.py
- site/pages.py
- README.md
- CHANGELOG.md
