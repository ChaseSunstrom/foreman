---
id: T-1858
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T20:01:58Z
updated: 2026-10-28T22:47:43Z
base: 22c2e7941f02552cd4dbba6591ba555ced624520
base_tree: edfa5dc4a849c26d08260d7839045d6c2ff0c998
plan0_at: 2026-10-28T22:36:42Z
plan0_scope: []
verified: strong
---
# Fm inbox swipe: a served swipe page through fm serve
## Raw request
> fm inbox swipe: a served swipe page through fm serve
## Interpretation
fm inbox swipe --serve: the deferred pile one card at a time in the browser (revive · keep · drop · skip), each answer applied as it is posted; fm serve is the headless systemd runner, so the page rides fm settings serve's loopback server instead (one-use token, cookie, Host/Origin checks, CSP, idle stop).
## Assumptions (confidence)
## Acceptance criteria
- [x] a card at a time, each answer applied at once, titles escaped, the page refuses a forged or batched post — verify with `python3 plugin/tests/run.py test_inbox_more`
- [x] fm settings serve still works unchanged; --serve goes with swipe alone — verify with `python3 plugin/tests/run.py test_settings_serve test_settings_room test_plugin_parity test_inbox_more`
## Non-goals
## Approach (options → choice → why)
Options: (1) a new HTTP server for the swipe page; (2) reuse fmsettingsserve with overridable draw/act/CMD/PATHS hooks on its Handler and a run() helper; (3) a static HTML file with JS posting to fm. Choice: 2 — every guard (token, cookie, Origin, CSP nonce, body cap, idle) is reused unchanged, the diff stays small, and no script runs on the page. 1 duplicates security code; 3 needs a server anyway.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for the served page (Served class)
2. [x] fmsettingsserve hooks + run(); swipe_page/swipe_post/swipe_server; --serve flag; backlog.md serve
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md backlog line, CHANGELOG.md entry, plugin/commands/backlog.md serve
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → ✗ exit 1 · Ran 14 tests in 4.2s (5 classes, 16 at a time; slowest: Swipe 4s, Served 3s, Pick 3s) / FAILED (1 classes) [ran] [tree d7ac7daf9a8f] (2026-10-28T22:37:01Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_settings_serve test_settings_room test_plugin_parity` → exit 0 · Ran 50 tests in 9.4s (11 classes, 16 at a time; slowest: Serve 9s, Served 5s, Page 4s) / OK [ran] [tree 667d693e9466] (2026-10-28T22:37:29Z)
- (step 3) `grep -c 'T-1858' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 6c04d8abc34b] (2026-10-28T22:37:35Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/lib/fmsettingsserve.py — commit it through a task, or git checkout it back / fm; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                  64.7    95.2     150  [0] / machine busy (load 1.1 per core): judged by each hook's CPU time, not wall time (T-0805) (slower: 33.1 s vs a usual 20.9 s); [ran] [tree 6c04d8abc34b] (2026-10-28T22:42:26Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_settings_serve test_settings_room test_plugin_parity` → exit 0 · Ran 51 tests in 9.0s (11 classes, 16 at a time; slowest: Serve 9s, Served 4s, Page 4s) / OK [ran] [tree 42f9e5555cf7] (2026-10-28T22:42:53Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/lib/fmsettingsserve.py — commit it through a task, or git checkout it back / fm; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.8    41.9     150  [0] / SessionEnd                  34.4    35.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 42f9e5555cf7] (2026-10-28T22:46:55Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 15 tests in 4.6s (5 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 1s) / OK [ran] [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (ac 2) `python3 plugin/tests/run.py test_settings_serve test_settings_room test_plugin_parity test_inbox_more` → exit 0 · Ran 51 tests in 9.0s (11 classes, 16 at a time; slowest: Serve 9s, Served 4s, Page 4s) / OK [ran] [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 15 tests in 4.6s (5 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 1s) / OK [ran] [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (audit intent) `one fm-reviewer pass (five lenses) over the diff; its 6 findings fixed, tests added, full gates green` → 'through fm serve' read as a served page on fm settings serve's loopback server (fm serve has no HTTP); logged [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (audit adversary) `one fm-reviewer pass (five lenses) over the diff; its 6 findings fixed, tests added, full gates green` → no findings; token, cookie, Host/Origin, CSP with no script, html.escape, one T-NNNN id per post [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (audit edge) `one fm-reviewer pass (five lenses) over the diff; its 6 findings fixed, tests added, full gates green` → a reload re-posting a keep is kept and logged once; --serve with --json or --apply refused; a stale drop is a 422 said [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (audit operator) `one fm-reviewer pass (five lenses) over the diff; its 6 findings fixed, tests added, full gates green` → no findings; idle stop at 30 minutes; hint wording fixed [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
- (audit maintainer) `one fm-reviewer pass (five lenses) over the diff; its 6 findings fixed, tests added, full gates green` → SWIPE_VERDICTS derived from SWIPE_KEYS; revive tested through the page; the mocked server closed [tree 42f9e5555cf7] (2026-10-28T22:47:16Z)
## Log
- 2026-10-28T20:01:58Z created
- 2026-10-28T22:36:42Z focused
- 2026-10-28T22:40:28Z decision: 'through fm serve' read as a served page; fm serve is the headless Remote Control runner (no HTTP), so the page rides fm settings serve's loopback server: loopback only, as settings serve is
- 2026-10-28T22:47:41Z done
- 2026-10-28T22:47:43Z committed fc2dd2e3 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- T-1659 [FEATURE M, done, 3 steps] fm settings serve: a loopback-only settings page from the schema, token required, writes through the settings setter — lesson: A loopba…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- similar finished tasks took 3–7 steps
## Lessons
- A served page reuses a hardened server by overriding hooks on its handler, never by copying its guards
## Plan gaps
- failed first: step 1 failing tests for the served page (Served class)
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/commands/backlog.md
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- plugin/lib/fmsettingsserve.py
- CHANGELOG.md
- MASTER.md
