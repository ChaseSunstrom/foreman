---
id: T-2312
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-31T10:32:24Z
updated: 2026-10-31T11:11:24Z
builder_model: sonnet
base: b67d45dc3f12d5a683e9dacb56aebc9888f206cc
base_tree: 966fe9bb4f351cc69917c2a4023087aaa8257863
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T10:45:11Z
plan0_scope: []
verified: strong
---
# fm lane merge and audit prep name every function the branch changes, so a stray edit stands out
## Raw request
> T-2311 (fm task evidence --repeat works again: _repeat_runs calls run_command with its own root) wasn't caught before it shipped: the builder's fm check --affected ran test_evidence_quality (the bench tests) but not test_verify_strength, which holds --repeat's tests in the same fmcli function family; and the builder edited with a script against the brief's Edit-only rule, so the rename spread beyond its function
## Interpretation
T-2303's rework changed _repeat_runs as well as _bench (a scripted rename spread), and both the main thread's read of the diff and the review missed the second site; ship73 caught it. Name each changed function from git's hunk headers in the merge result and in the review brief, so a function outside the task's plan is visible at a glance.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane merge's result and --json list the functions the branch changed per file (from git diff -U0 hunk headers against the merge base), and a branch that edits two functions in one file names both — verify with `python3 plugin/tests/run.py test_builder`
- [x] fm audit prep's review brief carries the same per-file function list under a 'Functions changed' line — verify with `python3 plugin/tests/run.py test_audit`
## Non-goals
## Approach (options → choice → why)
Options: 1) git's own hunk-header function context (diff -U0), no parsing of our own; 2) ast over the before/after files to map changed lines to defs; 3) only warn when a changed function isn't named in the brief's steps. Choice 1: one git call, works for any language git knows; 2 is Python-only and more code; 3 depends on step wording and would nag.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: a lane branch editing f and g in one file: merge output names both; the audit brief lists both
2. [x] A helper over git diff -U0 base...branch reading each hunk header's function context; print it in merge's result and json and write it into audit prep's brief
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder test_audit` → exit 0 · Ran 64 tests in 82.8s (25 classes, 16 at a time; slowest: Contract 80s, AuditRun 76s, DesignLens 60s) / OK [ran] [tree 67b90dbfa76b] (2026-10-31T10:50:55Z)
- (step 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 38 tests in 81.6s (17 classes, 16 at a time; slowest: AuditRun 79s, DesignLens 61s, ImportCards 29s) / OK [ran] [tree 67b90dbfa76b] (2026-10-31T10:52:19Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_verbs test_builder test_cli test_guard_cases test_lanes test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [146.20s] [ran] [tree 67b90dbfa76b] (2026-10-31T10:58:33Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_verbs test_builder test_cli test_guard_cases test_lanes test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.01s] [ran] [tree 8bf0818a4319] (2026-10-31T11:06:27Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_verbs test_builder test_cli test_guard_cases test_lanes test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.40s] [ran] [tree e8c6c634d954] (2026-10-31T11:07:49Z)
- (step 1) `python3 plugin/tests/run.py test_builder test_audit` → exit 0 · Ran 68 tests in 8.3s (25 classes, 16 at a time; slowest: Contract 8s, AuditRun 6s, DesignLens 6s) / OK [ran] [tree f4bf2ee302ba] (2026-10-31T11:08:25Z)
- (step 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 41 tests in 10.2s (17 classes, 16 at a time; slowest: AuditRun 10s, DesignLens 9s, ImportCards 5s) / OK [ran] [tree f4bf2ee302ba] (2026-10-31T11:08:35Z)
- `python3 plugin/tests/run.py test_builder test_audit` → ✗ exit 1 · Ran 68 tests in 8.4s (25 classes, 16 at a time; slowest: Contract 7s, AuditRun 6s, DesignLens 5s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree f4bf2ee302ba] (2026-10-31T11:08:57Z)
- `python3 plugin/tests/run.py test_builder test_audit` → exit 0 · Ran 68 tests in 12.9s (25 classes, 16 at a time; slowest: Contract 13s, AuditRun 11s, DesignLens 10s) / OK [ran] [tree f4bf2ee302ba] (2026-10-31T11:08:57Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 28 tests in 23.4s (9 classes, 16 at a time; slowest: Contract 23s, Brief 10s, LaneMergeGate 6s) / OK [ran] [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
- (ac 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 41 tests in 12.9s (17 classes, 16 at a time; slowest: AuditRun 12s, DesignLens 12s, ImportCards 6s) / OK [ran] [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
- (audit intent) `one fm-reviewer pass (adversary, edge, operator, maintainer): HIGH (a hunk header can be a column-0 credential line, unredacted in the reviewer prompt), MEDIUM (changed or added defs credited to the previous function), MEDIUM (methods collapse into their class: labeled honestly), LOWs (quoted names misattributed, silent caps, speed); all fixed by the builder; I asked for one more change (union of git's header and the hunk's defs unless the hunk starts on a def line), done with a test` → the merge and the review brief show every function a branch touched, so T-2303's stray _repeat_runs edit would have been named [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
- (audit adversary) `one fm-reviewer pass (adversary, edge, operator, maintainer): HIGH (a hunk header can be a column-0 credential line, unredacted in the reviewer prompt), MEDIUM (changed or added defs credited to the previous function), MEDIUM (methods collapse into their class: labeled honestly), LOWs (quoted names misattributed, silent caps, speed); all fixed by the builder; I asked for one more change (union of git's header and the hunk's defs unless the hunk starts on a def line), done with a test` → names pass c.redact and c.plain and are fitted; credential files are cut before parsing; git runs with fsmonitor and hooks off, no ext-diff or textconv; HEAD...branch can't read as an option [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
- (audit edge) `one fm-reviewer pass (adversary, edge, operator, maintainer): HIGH (a hunk header can be a column-0 credential line, unredacted in the reviewer prompt), MEDIUM (changed or added defs credited to the previous function), MEDIUM (methods collapse into their class: labeled honestly), LOWs (quoted names misattributed, silent caps, speed); all fixed by the builder; I asked for one more change (union of git's header and the hunk's defs unless the hunk starts on a def line), done with a test` → a def-line change names that def, an added function names itself, methods show their class (labeled), a git-quoted file resets the current file, caps say +N more [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
- (audit operator) `one fm-reviewer pass (adversary, edge, operator, maintainer): HIGH (a hunk header can be a column-0 credential line, unredacted in the reviewer prompt), MEDIUM (changed or added defs credited to the previous function), MEDIUM (methods collapse into their class: labeled honestly), LOWs (quoted names misattributed, silent caps, speed); all fixed by the builder; I asked for one more change (union of git's header and the hunk's defs unless the hunk starts on a def line), done with a test` → one extra -U0 diff per merge and audit prep; non-header lines skipped before any regex [tree 8f3c67fda29c] (2026-10-31T11:09:57Z)
## Log
- 2026-10-31T10:32:24Z created
- 2026-10-31T10:44:47Z planned from capture
- 2026-10-31T10:44:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2312.builder.md
- 2026-10-31T10:45:09Z focused
- 2026-10-31T10:45:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T11:08:15Z merged worktree-agent-a2d090e9b032f6892 (4 file(s))
- 2026-10-31T11:08:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2d090e9b032f6892
- 2026-10-31T11:08:15Z focused
- 2026-10-31T11:09:18Z scope: plugin/lib/fmlanes.py (functions_changed, merge), plugin/lib/fmcli.py (lane merge result, cmd_audit), plugin/tests/test_builder.py, plugin/tests/test_audit.py, MASTER.md, CHANGELOG.md
- 2026-10-31T11:11:21Z done
- 2026-10-31T11:11:24Z committed a1897c9f (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2311 [FIX S, done, 1 steps] fm task evidence --repeat works again: _repeat_runs calls run_command with its own root — lesson: A scripted rename spreads past the functi…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
## Lessons
- Make a review's surface explicit: listing every function a diff touches turns 'did anything else change?' into a glance
## Files touched
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- plugin/tests/test_builder.py
- plugin/tests/test_audit.py
- MASTER.md
- CHANGELOG.md
