---
id: T-2047
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:22:28Z
updated: 2026-10-29T23:20:35Z
base: 0a4b1aace4e892b3590f063282e894f6d6178b13
base_tree: c1aebdfa81841b725543bac92f83786ff4ef4b1d
plan0_at: 2026-10-29T22:53:22Z
plan0_scope: []
verified: strong
---
# fm lib check lints the checkout it runs in, not the installed plugin's cards
## Raw request
> fm lib check run inside a builder worktree lints the installed plugin's cards, not the worktree's; builders get a false clean result (--root didn't help)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check inside a checkout with plugin/skills/library/cards lints those cards; --root names one — verify with `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_check_lints_the_checkout_it_runs_in`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] fmlib check resolves the cards dir
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_check_lints_the_checkout_it_runs_in` → ✗ exit 1 · Ran 1 test in 0.331s / FAILED (failures=1) [ran] [tree 9a71ed29abae] (2026-10-29T22:53:43Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library` → exit 0 · Ran 42 tests in 12.599s / OK [ran] [tree 991330d9b8e7] (2026-10-29T22:54:04Z)
- `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_check_lints_the_checkout_it_runs_in` → ✗ exit 1 · Ran 1 test in 0.509s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ac3d3e9eecff] (2026-10-29T22:54:33Z)
- `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_check_lints_the_checkout_it_runs_in` → exit 0 · Ran 1 test in 0.162s / OK [ran] [tree ac3d3e9eecff] (2026-10-29T22:54:33Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmlib.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                27.4    29.5     150  [0] / SessionEnd                  23.8    25.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree ac3d3e9eecff] (2026-10-29T23:20:01Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_check_lints_the_checkout_it_runs_in` → exit 0 · Ran 1 test in 0.103s / OK [ran] [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit intent) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → a builder running fm lib check in its worktree now lints the worktree's cards, the false clean result is gone [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit adversary) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → --root is only joined and globbed; git runs via _git with an argument list; no exec of card content [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit edge) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → outside git or in a repo with no cards dir it falls back to the installed cards; a --root with none is a usage error, not a silent fallback [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit operator) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → one rev-parse per fm lib check; output unchanged in the main checkout (1219 cards) [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit maintainer) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → the resolution sits in the check branch only; other actions keep CARDS; the test builds a bad card in a temp repo [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
- (audit self) `self review of the 8-line diff: cards dir from --root or the cwd's git toplevel, falling back to the installed cards; proved red/green; gate exit 0, 4270 tests` → no findings [tree ac3d3e9eecff] (2026-10-29T23:20:11Z)
## Log
- 2026-10-29T20:22:28Z created
- 2026-10-29T22:53:21Z planned from capture
- 2026-10-29T22:53:21Z focused
- 2026-10-29T23:20:33Z done
- 2026-10-29T23:20:35Z committed e6c9c4bf (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- T-1175 [FIX S, done, 2 steps] Fm guard wrong run from a builder's worktree writes into the main checkout's corpus (PLUGI
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar finished tasks took 2–5 steps
## Why not caught
lint() and cards() defaulted to CARDS from PLUGIN_ROOT, and every test ran in the main checkout where the two paths agree
## Lessons
- A check that reads the plugin's own files must resolve them from the checkout under test, or worktrees get the installed copy's verdict
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmcli.py
- plugin/lib/fmlib.py
- CHANGELOG.md
