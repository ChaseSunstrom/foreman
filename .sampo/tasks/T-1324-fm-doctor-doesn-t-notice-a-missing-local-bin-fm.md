---
id: T-1324
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T03:18:24Z
updated: 2026-10-21T06:39:16Z
base: 330d4ea36d3eef1db4c1de6c7563fedeb886aebe
base_tree: ab079f9c6c5572f539efef406753e73582aeb4b1
plan0_at: 2026-10-21T06:31:10Z
plan0_scope: []
verified: strong
---
# fm doctor notices a missing or wrong ~/.local/bin/fm link and says the fix
## Raw request
> fm doctor doesn't notice a missing ~/.local/bin/fm link: the user's install predated it (T-0853), fm worked only inside Claude Code, and nothing said why ('how come fm isnt recognized as a command on my system?'); doctor should check it and offer the fix
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor's fm-link check passes when ~/.local/bin/fm points at this Foreman's plugin/bin/fm, and warns naming the fix (fm install-user) when it is missing or points elsewhere — verify with `python3 plugin/tests/run.py test_doctor`
- [x] with the link in place but ~/.local/bin not on PATH, it warns to add ~/.local/bin to PATH — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for check_fm_link (linked, missing, elsewhere, not on PATH)
2. [x] check_fm_link in fmdoctor, wired into fm doctor's results
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 52 tests in 47.2s (18 classes, 16 at a time; slowest: Command 47s, ViewsRepair 33s, Fix 2s) / FAILED (1 classes) [ran] [tree 488024aa5eee] (2026-10-21T06:32:10Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_doctor_fix` → exit 0 · Ran 52 tests in 49.0s (18 classes, 16 at a time; slowest: Command 49s, ViewsRepair 32s, Fix 2s) / OK [ran] [tree 04992b0fc924] (2026-10-21T06:33:09Z)
- `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 52 tests in 75.8s (18 classes, 16 at a time; slowest: Command 72s, ViewsRepair 54s, Fix 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 11459c0f88d7] (2026-10-21T06:36:11Z)
- `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 52 tests in 51.7s (18 classes, 16 at a time; slowest: Command 51s, ViewsRepair 35s, CardsAtPrompt 1s) / OK [ran] [tree 11459c0f88d7] (2026-10-21T06:36:11Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 52 tests in 51.7s (18 classes, 16 at a time; slowest: Command 51s, ViewsRepair 37s, Checks 1s) / OK [ran] [tree 11459c0f88d7] (2026-10-21T06:37:03Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 52 tests in 51.7s (18 classes, 16 at a time; slowest: Command 51s, ViewsRepair 37s, Checks 1s) / OK [ran] [tree 11459c0f88d7] (2026-10-21T06:37:03Z)
- (audit edge) `self: read the diff; three warnings each name their fix; PASS only when the link resolves to this Foreman's fm and its folder is on PATH; fm doctor --json shows PASS here` → someone else's fm at ~/.local/bin/fm is reported, never replaced (install-user also leaves it); a link through a symlinked home compares by realpath [tree 11459c0f88d7] (2026-10-21T06:37:03Z)
- (audit self) `self: read the diff; three warnings each name their fix; PASS only when the link resolves to this Foreman's fm and its folder is on PATH; fm doctor --json shows PASS here` → no findings [tree 11459c0f88d7] (2026-10-21T06:37:03Z)
## Log
- 2026-10-21T03:18:24Z created
- 2026-10-21T06:11:38Z planned from capture
- 2026-10-21T06:31:09Z focused
- 2026-10-21T06:34:01Z scope: CHANGELOG.md — its line; on this machine fm doctor --json reports fm link PASS (~/.local/bin/fm → plugin/bin/fm)
- 2026-10-21T06:39:13Z done
- 2026-10-21T06:39:16Z committed f84e7013 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-1332 [FEATURE M, done, 2 steps] Foreman notices on its own when a feature area needs a brainstorm and an improvement round — lesson: Friction is a signal to act on, no…
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Lessons
- Every install step that matters outside Claude Code (a link, a PATH entry) needs a doctor check, or an install from before it silently lacks it
## Plan gaps
- failed first: step 1 Failing tests for check_fm_link (linked, missing, elsewhere, not on PATH)
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
