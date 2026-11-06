---
id: T-0856
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T13:50:04Z
updated: 2026-10-15T14:04:19Z
base: 6fa3d4b91fe016e469537a9ee3adf12dc39b3457
base_tree: 94dc5ec9ee0749b0d078066864c5eed89ddc7176
verified: strong
---
# Foreman's one-shot claude -p children (relate, ideas, second, research) run with --no-sess
## Raw request
> Foreman's one-shot claude -p children (relate, ideas, second, research) run with --no-session-persistence, and fm tidy prunes the 528 leftover ~/.claude/projects/-run-user-*-fm-* folders they made (they clutter every resume picker)
## Interpretation
Claude Code makes a ~/.claude/projects/<encoded cwd>/ folder for every working directory a session starts in, persistence or not. Foreman's tool-less children (relate, ideas, second, research) each ran in a fresh temp dir, so 564 shells piled up (521 empty), cluttering resume pickers. Run them in one fixed private folder instead, and have fm tidy remove the empty shells.
## Assumptions (confidence)
## Acceptance criteria
- [x] children run in one fixed private folder (same path each time, 0700, ours, not a link); fm tidy --apply removes empty ~/.claude/projects shells of Foreman's child folders and keeps ones with files — verify with `python3 plugin/tests/run.py test_ideation test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests, then _child_dir and the tidy sweep
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ideation test_tidy` → exit 0 · Ran 18 tests in 1.8s (11 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree c43a546d5535] (2026-10-15T14:02:20Z)
- `python3 plugin/tests/run.py test_ideation test_tidy` → ✗ exit 1 · Ran 18 tests in 1.9s (11 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree c43a546d5535] (2026-10-15T14:02:24Z)
- `python3 plugin/tests/run.py test_ideation test_tidy` → exit 0 · Ran 18 tests in 1.8s (11 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree c43a546d5535] (2026-10-15T14:02:24Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmideas.py, plugin/lib/fmtidy.py — commit it through a task, or git checkout it back / fm doctor: OK (35 pass, 4 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.5    35.4     150  [0] / SessionEnd                  30.6    35.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree c43a546d5535] (2026-10-15T14:04:10Z)
- (ac 1) `python3 plugin/tests/run.py test_ideation test_tidy` → exit 0 · Ran 18 tests in 1.8s (11 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree c43a546d5535] (2026-10-15T14:04:18Z)
- (audit edge) `self: every Foreman child (relate, ideas, second, research) goes through fmideas.run_child/run_children, which now run in one private folder; tidy sweeps only empty shells whose names match Foreman's child folders` → the shared folder is refused (falls back to a temp dir) if it's a link, not ours, or not 0700 — a shared /tmp can't redirect children; shells holding any file (transcripts from fm second sessions, bench) are kept; the user's own project folders never match the -run-user-N-fm- / -tmp-fm- pattern [tree c43a546d5535] (2026-10-15T14:04:18Z)
- (audit self) `self: every Foreman child (relate, ideas, second, research) goes through fmideas.run_child/run_children, which now run in one private folder; tidy sweeps only empty shells whose names match Foreman's child folders` → no findings [tree c43a546d5535] (2026-10-15T14:04:18Z)
## Log
- 2026-10-15T13:50:04Z created
- 2026-10-15T14:01:33Z focused
- 2026-10-15T14:04:19Z done
- 2026-10-15T14:04:19Z committed 381720d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 2–5 steps
## Why not caught
none: found by the newcomer walkthrough noticing a stray projects folder
## Lessons
- Claude Code creates a projects folder per working directory even with --no-session-persistence: give background children one fixed cwd
## Files touched
- plugin/tests/test_ideation.py
- plugin/tests/test_tidy.py
- plugin/lib/fmideas.py
- plugin/lib/fmtidy.py
