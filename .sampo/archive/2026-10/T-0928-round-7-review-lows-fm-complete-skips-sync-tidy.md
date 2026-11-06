---
id: T-0928
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:39:50Z
updated: 2026-10-15T19:43:04Z
base: ce4667a4eda8cc28ee408aac125b7759ee63deda
base_tree: 97d4e6e514000b0a6e2783de7b5b4f419bdb87f8
verified: strong
---
# Round-7 review LOWs: fm complete skips sync; tidy backs up without holding the lock; doctor's state size leaves backups out; the claims gate counts only real test runs and ignores injected reminders; no 'nothing needed' line without criteria
## Raw request
> Round-7 review LOWs: fm complete skips sync; tidy backs up without holding the lock; doctor's state size leaves backups out; the claims gate counts only real test runs and ignores injected reminders; no 'nothing needed' line without criteria
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] each finding has a failing case first or a one-line reason — verify with `python3 plugin/tests/run.py -k Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests for findings 7, 8, 9; then the six fixes
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k Stop` → ✗ exit 1 · Ran 40 tests in 27.4s (1 classes, 16 at a time; slowest: Stop 27s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 747b947c7773] (2026-10-15T19:42:35Z)
- `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.2s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 747b947c7773] (2026-10-15T19:42:35Z)
- (ac 1) `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.2s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 747b947c7773] (2026-10-15T19:43:03Z)
- (step 1) `python3 plugin/tests/run.py -k Completion` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Completion 1s) / OK [ran] [tree 747b947c7773] (2026-10-15T19:43:03Z)
- (audit edge) `self: review findings 5-10 — fm complete skips the sync; tidy's backup runs without the project lock (seconds of gzip starved LOCK_QUICK hooks); doctor's state size leaves backups/ out (red first); the claims gate counts a runner only in command position, behind env assignments and launchers (cat pytest.ini, pip install pytest, cat run.py: red first); injected reminders (isMeta, <system-reminder>) don't restart the turn (red first); 'Nothing needed' needs at least one criterion. Finding 4 (the hook's TMPDIR vs the shell's) left: both inherit Claude Code's environment` → python3 plugin/tests/run.py, python3 -m pytest, ./gradlew test, FOO=1 pytest, fm quiet -- python3 …/run.py, bash -c "pytest" still count as runs [tree 747b947c7773] (2026-10-15T19:43:03Z)
- (audit self) `self: review findings 5-10 — fm complete skips the sync; tidy's backup runs without the project lock (seconds of gzip starved LOCK_QUICK hooks); doctor's state size leaves backups/ out (red first); the claims gate counts a runner only in command position, behind env assignments and launchers (cat pytest.ini, pip install pytest, cat run.py: red first); injected reminders (isMeta, <system-reminder>) don't restart the turn (red first); 'Nothing needed' needs at least one criterion. Finding 4 (the hook's TMPDIR vs the shell's) left: both inherit Claude Code's environment` → no findings [tree 747b947c7773] (2026-10-15T19:43:03Z)
## Log
- 2026-10-15T19:39:50Z created
- 2026-10-15T19:39:50Z focused
- 2026-10-15T19:43:04Z done
- 2026-10-15T19:43:04Z committed 44b66fa (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize. [stale: plugin/lib/fmsetup.py, plugin/uninstall.sh changed since it…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
## Files touched
- plugin/tests/test_hooks.py
- plugin/tests/test_doctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmtidy.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmcli.py
