---
id: T-1011
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T01:20:12Z
updated: 2026-10-16T01:29:19Z
base: e1c761bb76a5bf274706b0f139e2b0857c0e12f2
base_tree: 264cc73e41c99c35b671c5a0d2587873cf276061
verified: strong
---
# Self-docs check: every fm command is in one of fm help's tiers, so a close that adds a verb without one is refused
## Raw request
> T-1010 (Gates red since T-0974: fm approve-reads isn't in fm help's tiers (test_help, test_diff_ga) wasn't caught before it shipped: fm check labelled the red suite 'pre-existing' by command exit, so new failing tests inside an already-red command passed T-0974's close; compare failing test names, not the exit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] check_self_docs reports a command missing from HELP_TIERS (and one listed twice or not a command); the real repo passes — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a command missing from the tiers is a self-docs failure
2. [x] fmdoctor.check_self_docs compares fmcli.HELP_TIERS with the parser's commands
3. [x] docs: CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 42 tests in 23.0s (17 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, Checks 0s) / FAILED (1 classes) [ran] [tree 6babfa5e2bda] (2026-10-16T01:26:34Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_help` → exit 0 · Ran 46 tests in 23.7s (19 classes, 16 at a time; slowest: Command 24s, ViewsRepair 16s, Help 1s) / OK [ran] [tree c0f3c5e78645] (2026-10-16T01:27:06Z)
- (step 3) `grep -q 'T-1011' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 4aa39a553826] (2026-10-16T01:27:13Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_help` → exit 0 · Ran 46 tests in 23.1s (19 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, Help 1s) / OK [ran] [tree 01a3caeefae6] (2026-10-16T01:27:36Z)
- (audit edge) `self` → missing, duplicate and unknown names each reported; the real repo passes (test_self_docs_match_the_code); runs at close via _self_docs_gaps for any task touching fmcli.py [tree 01a3caeefae6] (2026-10-16T01:27:36Z)
- `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 42 tests in 22.9s (17 classes, 16 at a time; slowest: Command 22s, ViewsRepair 15s, Checks 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 01a3caeefae6] (2026-10-16T01:28:30Z)
- `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 42 tests in 22.6s (17 classes, 16 at a time; slowest: Command 22s, ViewsRepair 15s, Checks 0s) / OK [ran] [tree 01a3caeefae6] (2026-10-16T01:28:30Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 42 tests in 22.6s (17 classes, 16 at a time; slowest: Command 23s, ViewsRepair 15s, Checks 0s) / OK [ran] [tree 01a3caeefae6] (2026-10-16T01:28:53Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 42 tests in 22.8s (17 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, Checks 0s) / OK [ran] [tree 01a3caeefae6] (2026-10-16T01:29:16Z)
- (audit edge) `red→green on a patched HELP_TIERS; real repo passes` → duplicates and non-commands flagged too [tree 01a3caeefae6] (2026-10-16T01:29:16Z)
- (audit self) `red→green on a patched HELP_TIERS; real repo passes` → no findings [tree 01a3caeefae6] (2026-10-16T01:29:16Z)
## Log
- 2026-10-16T01:20:12Z created
- 2026-10-16T01:20:47Z corrected diagnosis: T-0974's step 3 ('run fm check and the e2e roundtrip') was satisfied by a narrower run (test_approve_reads test_guard test_hooks); the full suite, which holds test_help's every-command-in-a-tier invariant, never ran before its commit. Options: a step that names fm check accepts only fm check evidence; or fm check --affected links fmcli.py (new subparsers) to test_help/test_doctor; or finish --commit needs a passing fm check on a tree that changed plugin/lib
- 2026-10-16T01:20:48Z set tier=M
- 2026-10-16T01:26:01Z planned from capture
- 2026-10-16T01:26:01Z focused
- 2026-10-16T01:29:18Z done
- 2026-10-16T01:29:19Z committed 9fab934 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1010 [FIX S, done, 2 steps] Gates red since T-0974: fm approve-reads isn't in fm help's tiers (test_help, test_diff_ga
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one
- decision 2026-10-09: Self-approve T-0682 (FEATURE L, first versions)
- similar finished tasks took 2–2 steps
- start here (files T-1010 touched): plugin/lib/fmcli.py, plugin/tests/test_doctor.py
## Why not caught
none: this task is the catch
## Plan gaps
- failed first: step 1 red test: a command missing from the tiers is a self-docs failure
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- demo/live.cast
- demo/live.svg
- CHANGELOG.md
- demo/live.mp4
