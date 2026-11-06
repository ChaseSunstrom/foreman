---
id: T-2303
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T09:26:07Z
updated: 2026-10-31T10:17:57Z
builder_model: sonnet
base: afbb61d3044048d73e9a2c8bb1bdeeb3a1143457
base_tree: 3fcd5b97228fc713747d0251c59d052daef70bb2
plan0_at: 2026-10-31T09:41:02Z
plan0_scope: []
verified: strong
---
# fm task evidence --bench runs the start tree's own entry point when the command resolves into the tree
## Raw request
> fm task evidence --bench times CMD 'on the task's start tree', but a CMD that calls fm resolves it through PATH to the current code, so both sides time the same code (T-2298: 2.71 s -> 2.78 s, meaningless): put the start tree's plugin/bin first on PATH (and its lib on PYTHONPATH) for the before side, and say so when the CMD never touches the tree
## Interpretation
_bench times CMD in a throwaway worktree at the task's base, but a CMD like 'fm doctor' resolves fm through PATH (here a ~/.local/bin symlink into the current tree's plugin/bin), so both sides time the current code (T-2298: 2.71 s -> 2.78 s, no before at all).
## Assumptions (confidence)
## Acceptance criteria
- [x] When CMD's first word resolves through PATH (directly or via a symlink) to a file inside the project tree, the start-tree side runs that file's twin in the start worktree; a stub repo whose bin/tool prints a per-commit marker shows the before side ran the base copy and the after side the current one — verify with `python3 plugin/tests/run.py test_evidence_quality`
- [x] A CMD whose first word resolves outside the tree runs unchanged on both sides, and the result line says when neither side's entry point lies in the tree (a bench that may time the same code twice) — verify with `python3 plugin/tests/run.py test_evidence_quality`
## Non-goals
## Approach (options → choice → why)
Options: 1) resolve the first word with shutil.which, realpath it, and if it lies in p.root run the same relative path in the worktree; 2) prepend the worktree's bin folders to PATH; 3) refuse --bench commands that don't start with a relative path. Choice 1: follows symlinks (the real case), needs no guess at which folders are bin folders, and keeps every other command working; 3 would break plain commands.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test with a stub repo and a PATH symlink into it; then map the first word to its twin in _bench's before side, note when unmapped
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | tail -15` → exit 0 · Ran 17 tests in 4.4s (4 classes, 16 at a time; slowest: Bench 4s, Assume 2s, Inconclusive 1s) / OK [ran] [tree e8d050789416] (2026-10-31T09:41:51Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | tail -15` → exit 0 · Ran 17 tests in 4.4s (4 classes, 16 at a time; slowest: Bench 4s, Assume 2s, Inconclusive 1s) / OK [ran] [tree e8d050789416] (2026-10-31T09:41:51Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | tail -15` → exit 0 · Ran 17 tests in 4.4s (4 classes, 16 at a time; slowest: Bench 4s, Assume 2s, Inconclusive 1s) / OK [ran] [tree e8d050789416] (2026-10-31T09:41:51Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 17 tests in 4.5s (4 classes, 16 at a time; slowest: Bench 4s, Assume 2s, Inconclusive 1s) / OK [ran] [tree e8d050789416] (2026-10-31T09:41:58Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_evidence_quality test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.75s] [ran] [tree e8d050789416] (2026-10-31T09:42:31Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 20553a5aa902] (2026-10-31T09:43:39Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 20553a5aa902] (2026-10-31T09:43:39Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → exit 0 · OK [ran] [tree 7461b0827fdd] (2026-10-31T09:43:55Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → exit 0 · OK [ran] [tree 7461b0827fdd] (2026-10-31T09:43:55Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 18 tests in 4.8s (4 classes, 16 at a time; slowest: Bench 5s, Assume 2s, Inconclusive 1s) / OK [ran] [tree 7461b0827fdd] (2026-10-31T09:44:02Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_evidence_quality test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.56s] [ran] [tree 7461b0827fdd] (2026-10-31T09:44:36Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → ✗ exit 1 · FAILED (failures=2) / FAILED (1 classes) [ran] [tree 1b353327cab5] (2026-10-31T09:47:14Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion)"` → ✗ exit 1 · FAILED (failures=2) / FAILED (1 classes) [ran] [tree 1b353327cab5] (2026-10-31T09:47:14Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion|Traceback|\w*Error)"` → exit 0 · OK [ran] [tree 66aeef9e0745] (2026-10-31T09:47:44Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality 2>&1 | grep -E "^(FAIL|OK|Assertion|Traceback|\w*Error)"` → exit 0 · OK [ran] [tree 66aeef9e0745] (2026-10-31T09:47:44Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 19 tests in 9.9s (4 classes, 16 at a time; slowest: Bench 9s, Assume 3s, Inconclusive 2s) / OK [ran] [tree 66aeef9e0745] (2026-10-31T09:47:57Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_evidence_quality test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [52.19s] [ran] [tree 66aeef9e0745] (2026-10-31T09:49:42Z)
- (step 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 19 tests in 11.2s (4 classes, 16 at a time; slowest: Bench 11s, Assume 4s, Inconclusive 3s) / OK [ran] [tree 1ea224711c7e] (2026-10-31T10:15:40Z)
- `python3 plugin/tests/run.py test_evidence_quality` → ✗ exit 1 · Ran 19 tests in 11.1s (4 classes, 16 at a time; slowest: Bench 9s, Assume 3s, Inconclusive 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1ea224711c7e] (2026-10-31T10:16:05Z)
- `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 19 tests in 12.9s (4 classes, 16 at a time; slowest: Bench 12s, Assume 4s, Inconclusive 3s) / OK [ran] [tree 1ea224711c7e] (2026-10-31T10:16:05Z)
- (ac 1) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 19 tests in 14.3s (4 classes, 16 at a time; slowest: Bench 14s, Assume 4s, Inconclusive 3s) / OK [ran] [tree 397248500785] (2026-10-31T10:16:50Z)
- (ac 2) `python3 plugin/tests/run.py test_evidence_quality` → exit 0 · Ran 19 tests in 14.3s (4 classes, 16 at a time; slowest: Bench 14s, Assume 4s, Inconclusive 3s) / OK [ran] [tree 397248500785] (2026-10-31T10:16:50Z)
- (audit intent) `one fm-reviewer pass on the first-word version (intent MEDIUM: false 'neither side' note on python3 work.py; MEDIUM: FOO=1, time, pipes and chains missed; LOW: quoted first word silent); redesigned by the builder as a PATH shim for the before side, tests for each form added; I read the reworked diff: links only for PATH executables whose realpath lies under realpath(root)+sep, first match per name, env passed to run_command, notes only for names the command uses` → a before/after bench of a command that calls fm (or any tool resolving into the tree) now times the base code on the before side [tree 397248500785] (2026-10-31T10:16:50Z)
- (audit adversary) `one fm-reviewer pass on the first-word version (intent MEDIUM: false 'neither side' note on python3 work.py; MEDIUM: FOO=1, time, pipes and chains missed; LOW: quoted first word silent); redesigned by the builder as a PATH shim for the before side, tests for each form added; I read the reworked diff: links only for PATH executables whose realpath lies under realpath(root)+sep, first match per name, env passed to run_command, notes only for names the command uses` → nothing new executes (the shim links to the start tree's own files); the containment check uses realpath plus a separator so a look-alike folder isn't the tree [tree 397248500785] (2026-10-31T10:16:50Z)
- (audit edge) `one fm-reviewer pass on the first-word version (intent MEDIUM: false 'neither side' note on python3 work.py; MEDIUM: FOO=1, time, pipes and chains missed; LOW: quoted first word silent); redesigned by the builder as a PATH shim for the before side, tests for each form added; I read the reworked diff: links only for PATH executables whose realpath lies under realpath(root)+sep, first match per name, env passed to run_command, notes only for names the command uses` → FOO=1 tool, time tool, quoted tool, pipes and chains all reach the shim; a name new in the task is noted; fm|fm without spaces still shims but isn't matched for the notes [tree 397248500785] (2026-10-31T10:16:50Z)
- (audit operator) `one fm-reviewer pass on the first-word version (intent MEDIUM: false 'neither side' note on python3 work.py; MEDIUM: FOO=1, time, pipes and chains missed; LOW: quoted first word silent); redesigned by the builder as a PATH shim for the before side, tests for each form added; I read the reworked diff: links only for PATH executables whose realpath lies under realpath(root)+sep, first match per name, env passed to run_command, notes only for names the command uses` → one listdir and realpath per PATH executable per bench, negligible next to the timed runs [tree 397248500785] (2026-10-31T10:16:50Z)
## Log
- 2026-10-31T09:26:07Z created
- 2026-10-31T09:40:47Z planned from capture
- 2026-10-31T09:40:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2303.builder.md
- 2026-10-31T09:41:02Z focused
- 2026-10-31T10:15:25Z merged worktree-agent-a2eceea1c3597ab25 (2 file(s))
- 2026-10-31T10:15:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2eceea1c3597ab25
- 2026-10-31T10:15:26Z focused
- 2026-10-31T10:16:35Z scope: plugin/lib/fmcli.py (_bench shim), plugin/tests/test_evidence_quality.py, MASTER.md, CHANGELOG.md
- 2026-10-31T10:17:48Z done
- 2026-10-31T10:17:50Z committed f2a42707 (2 files)
- 2026-10-31T10:17:57Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2298 [PERFORMANCE M, done, 2 steps] fm doctor's usage burn and unloaded skills checks reuse their last result while their inputs are unchanged — lesson: A bench whose …
- T-2284 [FEATURE M, done, 3 steps] Measured perf proof (Mission 7, #6): fm task evidence ID --bench "<cmd>" times the command on the task's start tree and on the current …
- research T-1930-review: Approve. I could not break either claim. I read the code only and ran nothing, because this session has no Bash tool. [stale: plugin/tests/run.py…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
## Why not caught
T-2284's bench tests used relative commands that run per tree through the cwd; none called a tool through PATH, the common case
## Lessons
- A before/after harness must swap the code a command reaches, not just the cwd: PATH entry points and symlinks reach the current tree from anywhere
## Files touched
- plugin/tests/test_evidence_quality.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
