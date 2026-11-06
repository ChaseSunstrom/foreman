---
id: T-0859
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T14:11:10Z
updated: 2026-10-15T14:52:41Z
base: cdde03b75d3f837abe96db55dcc0154ae66983de
base_tree: d0dfb2c55506caaf9e103980a7640f670e5d3a0b
group: Guard command-analysis fixes
verified: strong
---
# Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 f
## Raw request
> Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 false blocks: S=$(cat f); mkdir -p $S/toy; cd $S/toy; git init), and the block names a rewrite (chain with && or git init "$S/toy")
## Interpretation
fmguard: 'S=$(cat f); mkdir -p $S/toy; cd $S/toy; git init -q' was blocked 3x as a tree write over core: the ';'-chained cd to an unresolvable dir leaves cwd = Foreman's repo (fmguard.py:2194-2201), bare git init writes '.' (2389-2391), and every git call goes through _tree_targets (2539-2546, 2264-2267). git init in a folder that is already a repo rewrites nothing the guard protects, and the refusal names no rewrite.
## Assumptions (confidence)
## Acceptance criteria
- [x] git init with no path in a cwd that already holds .git is not a tree write over core; the git-init block (when it still fires) hints: chain the cd with && or pass the path (git init "$S/toy"); the dangerous-form corpus stays blocked — verify with `python3 plugin/tests/run.py test_guard test_guard_diff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing guard test, then the git init exemption and hint
## Resume here
<!-- auto -->
- 2026-10-15T14:49:26Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard_git.py
- touched since last checkpoint: .claude/worktrees/agent-a25cba4d7b3d610e8/plugin/tests/test_guard_git.py, .claude/worktrees/agent-a25cba4d7b3d610e8/plugin/lib/fmguard.py, plugin/tests/test_guard_git.py, plugin/lib/fmguard.py
## Docs impact
CHANGELOG line added
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_git` → ✗ exit 1 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: GitChannels 0s) / FAILED (1 classes) [ran] [tree e9d5ff16923f] (2026-10-15T14:43:39Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git` → ✗ exit 1 · Ran 101 tests in 4.3s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / FAILED (1 classes) [ran] [tree 2e18bd27629e] (2026-10-15T14:44:02Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree ceb194b13807] (2026-10-15T14:44:17Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git` → exit 0 · Ran 101 tests in 4.3s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 56a5d47d084e] (2026-10-15T14:47:02Z)
- `python3 plugin/tests/run.py test_guard_git` → ✗ exit 1 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: GitChannels 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 56a5d47d084e] (2026-10-15T14:47:03Z)
- `python3 plugin/tests/run.py test_guard_git` → exit 0 · Ran 3 tests in 0.2s (1 classes, 16 at a time; slowest: GitChannels 0s) / OK [ran] [tree 56a5d47d084e] (2026-10-15T14:47:03Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.0    35.4     150  [0] / SessionEnd                  29.9    31.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 56a5d47d084e] (2026-10-15T14:48:55Z)
- (step 1) `python3 plugin/tests/run.py test_guard_git test_guard test_guard_diff` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree ffcdffee8321] (2026-10-15T14:50:24Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_diff` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree ffcdffee8321] (2026-10-15T14:52:27Z)
- (audit intent) `self review of the exemption plus a background security review (3 HIGH, all fixed): only git init / git init -q qualify, any GIT_* assignment or export in the command voids it` → a bare git init (or -q) where every resolved cwd already holds .git no longer refuses as a tree write over core; other forms keep refusing with a hint to chain the cd with && or pass the path [tree ffcdffee8321] (2026-10-15T14:52:27Z)
- (audit adversary) `self review of the exemption plus a background security review (3 HIGH, all fixed): only git init / git init -q qualify, any GIT_* assignment or export in the command voids it` → security review found long-option prefixes (--templ=, --sep=, --obj=, --ba), --shared/--bare and GIT_TEMPLATE_DIR / GIT_CONFIG_KEY_n=init.templateDir / export GIT_* could plant files; allow-list of -q/--quiet plus a GIT_\w*= scan over the whole command closes all; tests cover each form; fm replay 0 newly allowed [tree ffcdffee8321] (2026-10-15T14:52:27Z)
- (audit self) `self review of the exemption plus a background security review (3 HIGH, all fixed): only git init / git init -q qualify, any GIT_* assignment or export in the command voids it` → no findings [tree ffcdffee8321] (2026-10-15T14:52:27Z)
## Log
- 2026-10-15T14:11:10Z created
- 2026-10-15T14:43:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0859.builder.md
- 2026-10-15T14:43:13Z focused
- 2026-10-15T14:46:42Z merged worktree-agent-a25cba4d7b3d610e8 (2 file(s))
- 2026-10-15T14:46:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a25cba4d7b3d610e8
- 2026-10-15T14:46:42Z focused
- 2026-10-15T14:52:27Z done
- 2026-10-15T14:52:28Z committed f5e3ba5 (2 files)
- 2026-10-15T14:52:41Z includes T-0878: Catch it earlier: the guard had no notion of an idempotent re-init; every git init counted
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- the similar finished task took 2 steps
## Why not caught
the guard had no notion of an idempotent re-init; every git init counted as a write to its folder
## Plan gaps
- failed first: step 1 Failing guard test, then the git init exemption and hint
## Files touched
- plugin/tests/test_guard_git.py
- plugin/lib/fmguard.py
