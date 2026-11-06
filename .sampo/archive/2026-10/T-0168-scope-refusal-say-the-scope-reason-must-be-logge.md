---
id: T-0168
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_diff_gates.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T08:54:00Z
updated: 2026-10-03T09:07:09Z
base: 2cba7efabd01ff8f2f642767bb45c297b6b51179
base_tree: 485fbccd63d4fefea308d9a66092b1a342755468
verified: strong
---
# Scope refusal says the reason must be logged after the file's last edit, naming it
## Raw request
> Scope refusal: say the scope: reason must be logged after the last edit of the named file (scope_reason_covers); an earlier note doesn't count
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A refused finish names the out-of-scope file edited last and says a scope reason must come after that edit — verify with `python3 plugin/tests/run.py -k test_edits_outside_scope_need_a_reason`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red assertion
2. [x] The message
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_edits_outside_scope_need_a_reason` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: DiffGates 2s) / FAILED (1 classes) [ran] [tree ae0c1f8abc09] (2026-10-03T09:06:07Z)
- (step 1) `python3 plugin/tests/run.py -k test_edits_outside_scope_need_a_reason` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: DiffGates 2s) / OK [ran] [tree 6c7279162b08] (2026-10-03T09:06:16Z)
- (step 2) `python3 plugin/tests/run.py -k test_diff_gates -k test_round_f` → exit 0 · Ran 20 tests in 5.1s (2 classes, 16 at a time; slowest: DiffGates 5s, RoundF 1s) / OK [ran] [tree 6c7279162b08] (2026-10-03T09:06:22Z)
- (step 3) `grep -q T-0168 CHANGELOG.md` → exit 0 · (no output) [ran] [tree c3a3299fe1f6] (2026-10-03T09:07:01Z)
- (ac 1) `python3 plugin/tests/run.py -k test_edits_outside_scope_need_a_reason` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: DiffGates 2s) / OK [ran] [tree c3a3299fe1f6] (2026-10-03T09:07:09Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:07 UTC); cached (fm check --fresh reruns) [ran] [tree c3a3299fe1f6] (2026-10-03T09:07:09Z)
- (audit self) `self: red→green on the same test; the message names the out-of-scope file with the newest touch (the one a reason must follow) and says an earlier reason doesn't cover a later edit; text only, no rule changed` → no findings [tree c3a3299fe1f6] (2026-10-03T09:07:09Z)
## Log
- 2026-10-03T08:54:00Z created
- 2026-10-03T09:06:03Z planned from capture
- 2026-10-03T09:06:03Z focused
- 2026-10-03T09:07:09Z done
- 2026-10-03T09:07:09Z committed 6fdf4c6 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0164 [FIX S, done, 3 steps] A Bash touch is timed by the file's mtime, so a scope reason logged in the same command covers it — lesson: An async hook's own clock is th…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-0126-review: Verdict:** changes needed. Two gates can be skipped when a covered file changed (renames, and the wrapped-around skip chain). One skipped pass is…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
## Lessons
- A refusal that depends on timing must say the timing: 'say why' without 'after your last edit' sent me round twice.
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/lib/fmcli.py
- CHANGELOG.md
