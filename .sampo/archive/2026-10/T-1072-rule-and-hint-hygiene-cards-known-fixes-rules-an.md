---
id: T-1072
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmfixes.py, plugin/tests/test_tidy.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:40:25Z
base: a79ee93d54cd6e7f3ef309b21ecd64b07fdf05c2
base_tree: 69456129a3ed49b78a6a2215156eb70a6db78ec4
verified: strong
---
# Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel
## Raw request
> CLEAN: Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never helped in 60 days are listed by fm tidy and retired on a yes (wild C15)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm tidy` lists stack cards, known fixes, and lessons that never fired, or never helped, in 60 days. It retires them only with `--apply`. Covered in C15, in scope: ignored hints, card use ("card examples in CI" is not in scope), fix contraindications, and unused rules. Already present: card injection counts in `fm lib stats` (fmlib.py:812-832); fix tallies worked/misses/offered with a `_losing` check (fmfixes.py:241, `fixes-stats.json` has a `last` stamp); `retired_lessons` (fmrecall.py:453, retired via fmrecall.py:553); and guard rule fire counts (fmfriction.py:138). Hint "ignored" counts: `hints_quiet`, fmcore.py:2252.
## Assumptions (confidence)
## Acceptance criteria
- [x] A fix with no use in 60 days, or one that is losing, is listed by `fm tidy` and removed by `fm tidy --apply`. Unused cards are listed. — verify with `python3 plugin/tests/run.py test_tidy test_fixes`
## Non-goals
## Approach (options → choice → why)
(a) a new `fmhygiene.py`, (b) extend fmtidy `check_project`, (c) a `fm hygiene` command. Choice is (b). Add `_hygiene(p, apply, actions)` in fmtidy.py. Cards: the library minus the `card_injected` events in the ledger within 60 days. Fixes: `known(p)` joined with stats where `last` is older than 60 days or `_losing`. Lessons: skipped, because there is no fire record. Findings use severity "warn", with the fix text "fm tidy --apply retires". With `--apply`, fixes go through `fmfixes.remove`. Cards are only listed (retiring a shipped card file is not allowed), and the finding says so.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed `fixes-stats.json` with `last` 90 days old for fix A and fresh for fix B. Assert the dry run prints "stale_fix" for A only, and that `fm fix list` still shows A. Assert `--apply` removes A and not B. A `card_injected` event 5 days ago makes that card not listed; a card with none gets an "unused_card" finding.
2. [x] Implement `_hygiene` and call it from `check_project`; use `fmlib.cards()` and `fmfixes._stats_path`.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 19 tests in 4.2s (9 classes, 16 at a time; slowest: StalePlans 3s, Apply 3s, Repeats 3s) / FAILED (1 classes) [ran] [tree df756a3327d1] (2026-10-16T05:27:41Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_fixes` → ✗ exit 1 · Ran 33 tests in 7.8s (10 classes, 16 at a time; slowest: KnownFixes 8s, StalePlans 6s, Apply 6s) / FAILED (1 classes) [ran] [tree bd4f51ece1d3] (2026-10-16T05:27:56Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_fixes` → ✗ exit 1 · Ran 33 tests in 6.2s (10 classes, 16 at a time; slowest: KnownFixes 6s, StalePlans 4s, Apply 3s) / FAILED (1 classes) [ran] [tree 10fe4d3a3b42] (2026-10-16T05:28:06Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_fixes` → exit 0 · Ran 33 tests in 6.4s (10 classes, 16 at a time; slowest: KnownFixes 6s, StalePlans 5s, Apply 4s) / OK [ran] [tree a31174f0b2ae] (2026-10-16T05:28:24Z)
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 20 tests in 4.0s (9 classes, 16 at a time; slowest: StalePlans 4s, Apply 3s, Lanes 2s) / FAILED (1 classes) [ran] [tree 5c5fe7e61d40] (2026-10-16T05:36:35Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_fixes` → exit 0 · Ran 34 tests in 20.4s (10 classes, 16 at a time; slowest: KnownFixes 20s, StalePlans 10s, Apply 9s) / OK [ran] [tree 7a61a99cd73c] (2026-10-16T05:37:15Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy test_fixes` → exit 0 · Ran 34 tests in 4.7s (10 classes, 16 at a time; slowest: KnownFixes 5s, StalePlans 2s, Apply 2s) / OK [ran] [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (step 1) `python3 plugin/tests/run.py test_tidy test_fixes` → exit 0 · Ran 34 tests in 4.7s (10 classes, 16 at a time; slowest: KnownFixes 5s, StalePlans 2s, Apply 2s) / OK [ran] [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (audit intent) `review: one fm-reviewer pass (combined); 3 findings fixed by the builder test-first (no deletion of merely stale fixes + archive copy, synced fixes left alone, cards limited to the project's picked set read across rolled months)` → stale and losing fixes surface; only losing ones are retired [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (audit adversary) `review: one fm-reviewer pass (combined); 3 findings fixed by the builder test-first (no deletion of merely stale fixes + archive copy, synced fixes left alone, cards limited to the project's picked set read across rolled months)` → removal is reversible (archive copy); synced untrusted fixes never removed locally [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (audit edge) `review: one fm-reviewer pass (combined); 3 findings fixed by the builder test-first (no deletion of merely stale fixes + archive copy, synced fixes left alone, cards limited to the project's picked set read across rolled months)` → a fix with no stats record is kept; no map → no card claim [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (audit operator) `review: one fm-reviewer pass (combined); 3 findings fixed by the builder test-first (no deletion of merely stale fixes + archive copy, synced fixes left alone, cards limited to the project's picked set read across rolled months)` → one info finding for cards, not 1,084 rows [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
- (audit maintainer) `review: one fm-reviewer pass (combined); 3 findings fixed by the builder test-first (no deletion of merely stale fixes + archive copy, synced fixes left alone, cards limited to the project's picked set read across rolled months)` → _hygiene in fmtidy; card_injected read as enforce events with data kind [tree ff493ab8c27a] (2026-10-16T05:40:23Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:44Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmfixes.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T04:22:44Z set tier=M
- 2026-10-16T05:26:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1072.builder.md
- 2026-10-16T05:27:00Z focused
- 2026-10-16T05:40:06Z merged worktree-agent-aa397b9006bd5c987 (2 file(s))
- 2026-10-16T05:40:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa397b9006bd5c987
- 2026-10-16T05:40:07Z focused
- 2026-10-16T05:40:18Z scope: CHANGELOG.md — release note
- 2026-10-16T05:40:24Z done
- 2026-10-16T05:40:25Z committed e11b9e8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_fixes.py, plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmtidy.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Behaviour lock
test_tidy's existing classes (incl. test_clean_project_has_no_findings_that_need_action) pass unchanged; fm tidy without --apply still writes nothing; known fixes are only removed when losing, with a copy in archive/fixes-removed.md.
## Lessons
- A cleanup that deletes what users taught needs a reversible copy and a stronger signal than age
## Plan gaps
- failed first: step 1 Failing tests: seed `fixes-stats.json` with `last` 90 days old for fix A and fresh for fix B. Asser…
- failed first: step 2 Implement `_hygiene` and call it from `check_project`; use `fmlib.cards()` and `fmfixes._stats_path…
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
