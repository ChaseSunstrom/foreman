---
id: T-1047
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmeco.py, plugin/lib/fmcli.py, plugin/tests/test_ecosystem.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:09Z
updated: 2026-10-16T08:05:49Z
base: 8445b8814c67901c77918707c21cd03e5da54068
base_tree: cf7ed46ced1e713103e833702defad75a8a9c550
plan0_at: 2026-10-16T07:42:29Z
plan0_scope: [plugin/lib/fmeco.py, plugin/lib/fmcli.py, plugin/tests/test_ecosystem.py]
verified: strong
---
# Seed lessons and known fixes from git history (reverts, fix: commits) in fm adopt and on d
## Raw request
> Seed lessons and known fixes from git history (reverts, fix: commits) in fm adopt and on demand (T-1029 C2, C13)
## Interpretation
Foreman mines git history, meaning revert commits and "fix:" commits, into lessons recall can find, and into known fixes where the commit body carries an error and its remedy. It runs in `fm adopt` and on demand with `fm adopt --history` (C2, C13). Existing: `fmoutcomes.reverts` (`fmoutcomes.py:16`) lists Revert commits; recall indexes `research/*.md` (`fmrecall.py:90`); `fmfixes.add` stores fixes (`fmfixes.py:139`); `adopt()` (`fmeco.py:~60-148`) mines no history.
## Assumptions (confidence)
## Acceptance criteria
- [x] after `fm adopt` in a repo with a revert and a "fix:" commit, `fm recall` finds the lesson — verify with `python3 plugin/tests/run.py test_ecosystem test_fixes`
## Non-goals
## Approach (options → choice → why)
(a) write lessons into briefs (invasive); (b) write one `research/git-history-lessons.md` and add fixes with `fmfixes.add`; (c) a separate command. Choose (b) with the flag on the existing `adopt` command: recall already reads research notes, and re-running is idempotent (the note is rewritten, `add` dedups by id).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a temp repo with `Revert "x"` and `fix: crash on empty input` (body "error: IndexError → guard len"); `fm adopt` writes `research/git-history-lessons.md` listing both; `fm fix list` shows the body-pair as a fix; second run adds nothing; a repo with no such commits writes no note.
2. [x] `fmeco.seed_history(p)`: `git log -n 300 --format=%H%x00%s%x00%b`, subjects matching `^(fix|revert)`, each with its files; the body regexp `error: (.+?) → (.+)` feeds `fmfixes.add`. Call from `adopt()` and from `cmd_adopt` when `--history` is set, redacting with `c.redact`/`c.defang`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ecosystem` → ✗ exit 1 · Ran 15 tests in 9.8s (8 classes, 16 at a time; slowest: HarnessCanary 9s, Sweep 4s, MachineIdentity 2s) / FAILED (1 classes) [ran] [tree f326b6480119] (2026-10-16T07:42:59Z)
- (step 1) `python3 plugin/tests/run.py test_ecosystem test_fixes` → exit 0 · Ran 29 tests in 14.1s (9 classes, 16 at a time; slowest: KnownFixes 14s, HarnessCanary 8s, Sweep 5s) / OK [ran] [tree 45d73aebf3db] (2026-10-16T07:45:41Z)
- (step 2) `python3 plugin/tests/run.py test_ecosystem test_fixes` → exit 0 · Ran 29 tests in 7.0s (9 classes, 16 at a time; slowest: KnownFixes 7s, HarnessCanary 5s, Sweep 3s) / OK [ran] [tree 45d73aebf3db] (2026-10-16T07:45:49Z)
- (step 2) `python3 plugin/tests/run.py test_ecosystem test_fixes` → exit 0 · Ran 30 tests in 5.9s (9 classes, 16 at a time; slowest: KnownFixes 6s, HarnessCanary 4s, Sweep 2s) / OK [ran] [tree 6afb1d6dfffd] (2026-10-16T07:48:37Z)
- (step 2) `python3 plugin/tests/run.py test_ecosystem test_fixes` → exit 0 · Ran 33 tests in 4.7s (9 classes, 16 at a time; slowest: KnownFixes 5s, HarnessCanary 3s, Sweep 2s) / OK [ran] [tree b5ee2a235fcb] (2026-10-16T07:56:46Z)
- (step 1) `python3 plugin/tests/run.py test_ecosystem test_fixes test_claims test_bus test_builder test_lanes test_night test_recall test_tidy` → exit 0 · Ran 179 tests in 27.4s (54 classes, 16 at a time; slowest: Recall 27s, Lanes 23s, Contract 20s) / OK [ran] [tree 3255593b4058] (2026-10-16T08:04:35Z)
- (ac 1) `python3 plugin/tests/run.py test_ecosystem test_fixes` → exit 0 · Ran 33 tests in 4.8s (9 classes, 16 at a time; slowest: KnownFixes 5s, HarnessCanary 3s, Sweep 2s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:05:00Z)
- (audit intent) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: commit text was a trusted fix → trust=False, project store only, hint until fm fix trust; quadratic body regex → per line, 2,000 chars; best() could prefer a repo hint → trusted first; --> made the id unstable, so a rerun re-added → _clean before the id. All fixed test-first on the builder's branch; 179 merged tests pass` → history becomes a recall note plus hint fixes [tree acc2d51590ee] (2026-10-16T08:05:00Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: commit text was a trusted fix → trust=False, project store only, hint until fm fix trust; quadratic body regex → per line, 2,000 chars; best() could prefer a repo hint → trusted first; --> made the id unstable, so a rerun re-added → _clean before the id. All fixed test-first on the builder's branch; 179 merged tests pass` → a malicious commit body can't become a trusted instruction (tested with a curl|sh remedy) [tree acc2d51590ee] (2026-10-16T08:05:00Z)
- (audit edge) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: commit text was a trusted fix → trust=False, project store only, hint until fm fix trust; quadratic body regex → per line, 2,000 chars; best() could prefer a repo hint → trusted first; --> made the id unstable, so a rerun re-added → _clean before the id. All fixed test-first on the builder's branch; 179 merged tests pass` → 500 KB body line, a second run adds 0, no matching commits writes no note [tree acc2d51590ee] (2026-10-16T08:05:00Z)
- (audit operator) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: commit text was a trusted fix → trust=False, project store only, hint until fm fix trust; quadratic body regex → per line, 2,000 chars; best() could prefer a repo hint → trusted first; --> made the id unstable, so a rerun re-added → _clean before the id. All fixed test-first on the builder's branch; 179 merged tests pass` → fm adopt --history runs alone [tree acc2d51590ee] (2026-10-16T08:05:00Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge) plus the automated commit security review: commit text was a trusted fix → trust=False, project store only, hint until fm fix trust; quadratic body regex → per line, 2,000 chars; best() could prefer a repo hint → trusted first; --> made the id unstable, so a rerun re-added → _clean before the id. All fixed test-first on the builder's branch; 179 merged tests pass` → seed_history in fmeco, trust flag on fmfixes.add [tree acc2d51590ee] (2026-10-16T08:05:00Z)
## Log
- 2026-10-16T03:42:09Z created
- 2026-10-16T04:22:56Z set scope=['plugin/lib/fmeco.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_ecosystem.py']
- 2026-10-16T04:22:57Z set tier=M
- 2026-10-16T07:42:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1047.builder.md
- 2026-10-16T07:42:28Z focused
- 2026-10-16T08:03:25Z merged worktree-agent-a1c4207ff93ff7e7d (4 file(s))
- 2026-10-16T08:03:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1c4207ff93ff7e7d
- 2026-10-16T08:04:06Z focused
- 2026-10-16T08:04:55Z scope: MASTER.md, CHANGELOG.md — docs for T-1047, T-1068, T-1071
- 2026-10-16T08:05:48Z done
- 2026-10-16T08:05:49Z committed 7b38361 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- decision 2026-10-09: Self-approved T-0685 (L): three model-free first versions on existing data (recall multipliers, a lesion report, a dream file); the self-critique fo…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_ecosystem.py; re-ground the plan against them before editing
## Lessons
- Text from a repo (commits, issues, docs) enters as a hint the user can promote, never as an instruction
## Plan gaps
- failed first: step 1 Failing tests: a temp repo with `Revert "x"` and `fix: crash on empty input` (body "error: IndexErr…
## Files touched
- plugin/tests/test_ecosystem.py
- plugin/lib/fmeco.py
- plugin/lib/fmcli.py
- plugin/lib/fmfixes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbus.py
- plugin/lib/fmlanes.py
- plugin/lib/fmnight.py
- plugin/lib/fmrecall.py
- plugin/lib/fmtidy.py
- plugin/tests/test_claims.py
- plugin/tests/test_night.py
- plugin/tests/test_recall.py
