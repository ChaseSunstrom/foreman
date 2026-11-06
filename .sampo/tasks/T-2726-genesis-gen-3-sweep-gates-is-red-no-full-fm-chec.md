---
id: T-2726
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T23:42:30Z
updated: 2026-11-03T00:04:24Z
genesis_sweep: 3:gates
base: 33a6416b66a691555d7bd1cf921cefed0b18ae0c
base_tree: 9348380af51e2410252b973cca2452d1dc2fe253
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:49:17Z
plan0_scope: []
verified: strong
---
# Genesis gen-3 sweep: gates is red — no full fm check pass recorded on this exact tree: run fm check
## Raw request
> fm genesis sweep 3: ✗ gates: no full fm check pass recorded on this exact tree: run fm check
> Done when the rerun's gates line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep's gates line is ✓ — verify with `grep -q '^✓ gates:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix what the sweep's gates line names, then rerun fm genesis sweep 3
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `grep -q '^✓ gates:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:21Z)
- (step 1) `grep -q '^✓ gates:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:22Z)
- (ac 1) `grep -q '^✓ gates:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:04:22Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:23Z)
- (audit operator) `ran fm check on the tree holding every gen-3 sweep fix: all gates exit 0 (5816 tests OK, roundtrip 17/17, bench under budget); the rerun sweep reads 'full gates green on this tree'` → the gates row needed a full fm check on this exact tree, so it ran after T-2725 and T-2727's edits [tree 9348380af51e] (2026-11-03T00:04:23Z)
- (audit self) `ran fm check on the tree holding every gen-3 sweep fix: all gates exit 0 (5816 tests OK, roundtrip 17/17, bench under budget); the rerun sweep reads 'full gates green on this tree'` → no findings [tree 9348380af51e] (2026-11-03T00:04:23Z)
## Log
- 2026-11-02T23:42:30Z created
- 2026-11-02T23:49:16Z focused
- 2026-11-02T23:49:17Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T00:04:16Z criterion 1 verify: `fm genesis sweep 3` → `grep -q '^✓ gates:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
- 2026-11-03T00:04:24Z done
## Follow-ups captured
## Regression test
none: the gates row reads a recorded full fm check on the tree; its check is the criterion
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-11-01: [confidence: 75%] Fold six verbs (proof, triggers, calibration, incident, sweep, instruments) into prove, outcomes, capture, projects and which, and…
