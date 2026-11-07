---
id: T-1879
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-28T23:20:21Z
base: c3d766f110d8a130f50cc9c4145cec06e4a48610
base_tree: c92e4dc17a138074ab7ba5093006054023c0ae54
plan0_at: 2026-10-28T23:06:25Z
plan0_scope: []
verified: strong
---
# Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f
## Raw request
> CLEAN: robustness sweep: every state-reading verb survives a malformed brief or meta (truncated frontmatter, binary bytes) without a traceback, and mutating verbs run twice are no-ops
> CONTEXT: forever loop round 5 ("Fuzz every file-reading verb with malformed content", "Run every mutating verb twice and assert the second run is a no-op").
## Interpretation
Fuzz the state Foreman reads: a brief with truncated frontmatter, binary bytes or wrong-typed fields, and a corrupt meta.json, must never make a read verb (status, queue, next, inbox, digest, task list/show, tidy) print a traceback; corrupt meta gives the CorruptState message. Mutating verbs run twice (drive off, sensitive on, drop of a dropped task, tidy --apply, the same capture) leave state as the first run left it.
## Assumptions (confidence)
## Acceptance criteria
- [x] no read verb tracebacks on a malformed brief or meta, and mutating verbs run twice leave state unchanged — verify with `python3 plugin/tests/run.py test_robustness`
## Non-goals
## Approach (options → choice → why)
1) a property fuzzer over every verb (big, slow, flaky); 2) one test file driving the verbs a user runs most against a fixed set of malformed files, fixing each traceback at its shared reader; 3) a top-level except in fm's main. Choice: 2, plus fixing root causes in the shared loaders, not 3 (a blanket catch hides real bugs).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: malformed briefs/meta across read verbs; mutating verbs twice
2. [x] fix each traceback at its shared reader
3. [x] docs: CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T23:13:02Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmtidy.py, plugin/tests/test_robustness.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/rb.sh, plugin/lib/fmtidy.py, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_robustness.py
- failures met: fm: warning: verify command `true`: it can't fail (nothing in it checks the behaviour)
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_robustness 2>&1 | grep -B2 -A6 "^AssertionError\|^FAIL:" | head -30` → ✗ exit 1 · Ran 2 tests in 3.688s / FAILED (failures=1) [ran] [tree 0dbbcd663b2e] (2026-10-28T23:09:14Z)
- (step 1) `python3 plugin/tests/run.py test_robustness` → exit 0 · Ran 2 tests in 4.3s (1 classes, 16 at a time; slowest: Robustness 4s) / OK [ran] [tree 3baa0f7e4804] (2026-10-28T23:10:27Z)
- (step 2) `python3 plugin/tests/run.py test_robustness test_tidy test_drill` → exit 0 · Ran 46 tests in 6.1s (16 classes, 16 at a time; slowest: DeferredTriage 6s, StalePlans 6s, Robustness 5s) / OK [ran] [tree 3baa0f7e4804] (2026-10-28T23:10:33Z)
- (step 3) `grep -c T-1879 CHANGELOG.md` → exit 0 · 1 [ran] [tree 3baa0f7e4804] (2026-10-28T23:10:33Z)
- (step 2) `python3 plugin/tests/run.py test_robustness test_tidy test_drill` → exit 0 · Ran 47 tests in 8.8s (16 classes, 16 at a time; slowest: Robustness 9s, DeferredTriage 6s, StalePlans 6s) / OK [ran] [tree a1f7a82214fc] (2026-10-28T23:14:59Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmtidy.py — commit it through a task, or git checkout it back / fm doctor:; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.6    44.4     150  [0] / SessionEnd                  34.6    37.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree a1f7a82214fc] (2026-10-28T23:18:58Z)
- (ac 1) `python3 plugin/tests/run.py test_robustness` → exit 0 · Ran 3 tests in 7.9s (1 classes, 16 at a time; slowest: Robustness 8s) / OK [ran] [tree a1f7a82214fc] (2026-10-28T23:19:17Z)
- (audit intent) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → read verbs and the five hooks survive six malformed briefs and a cut-off or binary meta.json; six mutating verbs run twice change nothing the second time [tree a1f7a82214fc] (2026-10-28T23:19:17Z)
- (audit adversary) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → a repeat with new words or a new --until still records; a first run must exit 0, so two equal failures can't pass as idempotence [tree a1f7a82214fc] (2026-10-28T23:19:17Z)
- (audit edge) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → a view differing only in its Generated line isn't rewritten (no fsync); tidy --apply stamps last_tidy before the views so STATE.md never says never; meta read as UTF-8 whatever the locale [tree a1f7a82214fc] (2026-10-28T23:19:17Z)
- (audit intent) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → read verbs and the five hooks survive six malformed briefs and a cut-off or binary meta.json; six mutating verbs run twice change nothing the second time [tree a1f7a82214fc] (2026-10-28T23:19:53Z)
- (audit adversary) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → a repeat with new words or a new --until still records; a first run must exit 0, so two equal failures can't pass as idempotence [tree a1f7a82214fc] (2026-10-28T23:19:53Z)
- (audit edge) `one fm-reviewer pass (research T-1879-review): 2 medium, 4 low; all fixed test-first or noted` → a view differing only in its Generated line isn't rewritten (no fsync); tidy --apply stamps last_tidy before the views so STATE.md never says never; meta read as UTF-8 whatever the locale [tree a1f7a82214fc] (2026-10-28T23:19:53Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-28T23:06:25Z focused
- 2026-10-28T23:19:44Z includes T-1880: Read_meta` (plugin/lib/fmcore.py:741) opens `meta.json` without `encoding=`, so it depends
- 2026-10-28T23:20:19Z done
- 2026-10-28T23:20:21Z committed 5d776079 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Terminal and mod UI (fm playbooks show ui/terminal-ui)
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- research mission-20261016-071058: Request: forever loop round 4: improve past everything shipped [stale: demo/live.mp4, demo/live.svg, plugin/tests/bench_hooks.py change…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- the similar finished task took 4 steps
## Behaviour lock
none: the suite wasn't run before the first edit; the existing suites over these paths (test_tidy, test_drill, test_cli) pass unchanged after it, and the full gate (4087 tests) passed on the final tree
## Lessons
- An idempotence check compares what the verb logs, suffixes included: block --until logs (revisit DATE), so a match on the reason alone missed it. A CLEAN task records its behaviour lock (step 1 tests) before the first edit.
## Files touched
- plugin/tests/test_robustness.py
- plugin/lib/fmcore.py
- plugin/lib/fmtidy.py
- plugin/lib/fmcli.py
- CHANGELOG.md
