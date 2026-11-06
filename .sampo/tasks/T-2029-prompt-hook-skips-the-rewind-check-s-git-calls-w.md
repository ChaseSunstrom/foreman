---
id: T-2029
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T18:50:37Z
updated: 2026-10-29T18:59:06Z
base: 4d76875b0c674da7998debc025f89dd3f1d1b075
base_tree: 75a95f977da062872fc8d62ec45b73a1b5a9079e
plan0_at: 2026-10-29T18:51:45Z
plan0_scope: []
verified: strong
---
# Prompt hook skips the rewind check's git calls when no step has a proof, and reuses its one brief load
## Raw request
> Prompt hook skips the rewind check's git calls when no step has a proof, and reuses its one brief load
## Interpretation
Each prompt runs reconcile_rewind: one active_brief_fast pass (index load + 1201 stats) and worktree_tree (3 git subprocesses, ~10-18 ms), then load_briefs again right after. rewound() can only reopen a step with a passing proof, so with none the git work is wasted; and the caller already loads every brief.
## Assumptions (confidence)
## Acceptance criteria
- [x] reconcile_rewind runs no git when the active task has no passing step proof, and takes the caller's briefs instead of a second scan — verify with `python3 plugin/tests/run.py test_rewind`
## Non-goals
## Approach (options → choice → why)
Options: (a) in reconcile_rewind return None before worktree_tree when no step has a passing proof with a tree mark, and accept briefs= from the caller (load first, reload only if it reopened); (b) cache worktree_tree by index/dir stats: unsafe, edits don't move dir mtimes; (c) move the rewind check to Stop only: a /rewind before a prompt would then go unseen until the turn ends. Chose (a). Rejected (b) unsafe, (c) loses the prompt-time reopen.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: no worktree_tree call without a passing proof; briefs passed in are used, no active_brief_fast
2. [x] Implement in fmcore.reconcile_rewind and fmhooks.user_prompt_submit; CHANGELOG with numbers
## Resume here
<!-- auto -->
- 2026-10-29T18:52:22Z step 1/2: Red tests: no worktree_tree call without a passing proof; briefs passed in are used, no active_brief_fast
- git: foreman/build; 3 uncommitted: plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_rewind.py
- touched since last checkpoint: plugin/tests/test_rewind.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit29.json, plugin/lib/fmcore.py, plugin/lib/fmhooks.py
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_rewind 2>&1 | grep -E "Error|assert|FAIL|OK|Ran" | head -8` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: Rewind 3s) / FAILED (1 classes) [ran] [tree 6e020f608fd4] (2026-10-29T18:51:58Z)
- (ac 1) `python3 plugin/tests/run.py test_rewind 2>&1 | grep -E "Error|assert|FAIL|OK|Ran" | head -8` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: Rewind 3s) / FAILED (1 classes) [ran] [tree 5417af68f20b] (2026-10-29T18:52:10Z)
- (step 1) `python3 plugin/tests/run.py test_rewind` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: Rewind 3s) / FAILED (1 classes) [ran] [tree 5417af68f20b] (2026-10-29T18:52:16Z)
- (step 2) `python3 plugin/tests/run.py test_rewind test_hooks` → exit 0 · Ran 211 tests in 32.8s (28 classes, 16 at a time; slowest: Stop 33s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree 2988972c5e1f] (2026-10-29T18:54:33Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py, plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.2    31.5     150  [0] / SessionEnd                  25.5    26.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 2988972c5e1f] (2026-10-29T18:58:11Z)
- (ac 1) `python3 plugin/tests/run.py test_rewind` → exit 0 · Ran 5 tests in 3.7s (1 classes, 16 at a time; slowest: Rewind 3s) / OK [ran] [tree 2988972c5e1f] (2026-10-29T18:58:27Z)
- (step 1) `python3 plugin/tests/run.py test_rewind` → exit 0 · Ran 5 tests in 3.7s (1 classes, 16 at a time; slowest: Rewind 3s) / OK [ran] [tree 2988972c5e1f] (2026-10-29T18:58:27Z)
- (audit intent) `self-review of the diff: the early return accepts any non-failed evidence row with a tree mark (step or ac), a superset of what rewound() needs, so it never skips a reopen; the caller's briefs hold the active brief fully parsed (stubs are closed briefs only)` → prompts still reconcile on every turn once a step is proved; SessionStart and fm state keep their own scan [tree 2988972c5e1f] (2026-10-29T18:58:27Z)
- (audit edge) `self-review of the diff: the early return accepts any non-failed evidence row with a tree mark (step or ac), a superset of what rewound() needs, so it never skips a reopen; the caller's briefs hold the active brief fully parsed (stubs are closed briefs only)` → a rewind mutates the caller's brief object, so the hook reloads briefs only then; a lane's active task is found by active_brief(briefs, lane) as before [tree 2988972c5e1f] (2026-10-29T18:58:27Z)
## Log
- 2026-10-29T18:50:37Z created
- 2026-10-29T18:51:45Z focused
- 2026-10-29T18:59:05Z done
- 2026-10-29T18:59:06Z committed 7cfd9eaa (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- T-1267 [FEATURE M, done, 2 steps] Reconcile Foreman's state after /rewind and /clear; flag CLAUDE.md or memory rules that co — lesson: Second-resolution timestamps can't…
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
## Measurements
UserPromptSubmit median 94 -> 77 ms (hook_t, 15 runs, A/B against HEAD's fmcore/fmhooks, twice: 94/77, 94/76) while the active task has no passing proof; with one, the second brief scan (~13 ms profiled) is still saved
## Lessons
- A check that needs a precondition (a passing proof) should test it before paying for subprocesses; and a hook that already loaded briefs should hand them down instead of letting callees rescan
## Plan gaps
- failed first: step 1 Red tests: no worktree_tree call without a passing proof; briefs passed in are used, no active_brie…
## Files touched
- plugin/tests/test_rewind.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
