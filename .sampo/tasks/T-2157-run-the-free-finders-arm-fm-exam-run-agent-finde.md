---
id: T-2157
type: RESEARCH
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T14:08:41Z
updated: 2026-10-30T14:23:03Z
base: 93cf6b98ca3e041163ae36c47d9d4c54e156b922
base_tree: de28690094e607e9a28f79eb579e8b51049e7ef9
plan0_at: 2026-10-30T14:11:09Z
plan0_scope: []
paused_tree: de28690094e607e9a28f79eb579e8b51049e7ef9
verified: ok
---
# Run the free finders arm (fm exam run --agent finders) on every scenario of the run…
## Raw request
> Run the free finders arm (fm exam run --agent finders) on every scenario of the run behind the 0/108 baseline now, since fm find shipped after it; file the result in the tower and compare against the baseline (steer 2026-10-30 rule 1)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the finders arm has graded every s0-001 scenario (split all) and its row is in exam.jsonl — verify with `fm exam status --json`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm exam run s0-001 --agent finders --split all, then fm exam grade s0-001
2. [x] file the found count vs the 0/108 baseline in the tower (critique-exam.md revisit row) via fm genesis put
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm exam status` → exit 0 · oracle s31-006: 18/18 found, 0 false alarms, 18/18 fixed, 6/6 test-first, 3/3 ranked, held out 18/18 found / finders s0-001: 90/108 found, 0 false alarms, 0/108 fixed, 0/54 test-first, 0/18 readings, [ran] [tree de28690094e6] (2026-10-30T14:12:33Z)
- (ac 1) `fm exam status --json` → exit 0 · ] / } [ran] [tree de28690094e6] (2026-10-30T14:12:34Z)
- (step 2) `grep -c 'T-2157' state/projects/foreman-4a056f/research/genesis/gen-1/critique-exam.md` → exit 0 · 2 [ran] [tree de28690094e6] (2026-10-30T14:12:34Z)
- (audit self) `self` → ran an existing zero-token arm on s0-001 split all; result read from exam status and filed through fm genesis put (critique-exam.md revisit row); no code touched [tree de28690094e6] (2026-10-30T14:14:06Z)
- (ac 1) `fm exam status --json` → exit 0 · ] / } [ran] [tree de28690094e6] (2026-10-30T14:14:07Z)
- `fm exam status` → exit 0 · oracle s31-006: 18/18 found, 0 false alarms, 18/18 fixed, 6/6 test-first, 3/3 ranked, held out 18/18 found / finders s0-001: 90/108 found, 0 false alarms, 0/108 fixed, 0/54 test-first, 0/18 readings, [ran] [tree de28690094e6] (2026-10-30T14:14:07Z)
- (audit self) `self: zero-token finders arm on s0-001, result filed in critique-exam.md` → no findings [tree de28690094e6] (2026-10-30T14:14:07Z)
- (audit self) `self: the finders arm ran on s0-001 (90/108 found, 0 false alarms, held out 30/36); the critique-exam.md Finders row and bullet carry the result; the Decision names what would change it` → no findings [tree 66bb16552a55] (2026-10-30T14:23:02Z)
## Log
- 2026-10-30T14:08:41Z created
- 2026-10-30T14:10:06Z planned: it has criteria and steps
- 2026-10-30T14:11:08Z focused
- 2026-10-30T14:14:18Z paused: focus moved to T-2165
- 2026-10-30T14:23:03Z done
## Follow-ups captured
## Behaviour lock
none: runs an existing zero-token exam arm and files its result; no code change
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- decision 2026-10-30: [revisited: Exam baseline: the finders arm (fmdocs.scan + fmsecrets, no session) scores 0/108 on s0-001] Exam baseline stays: the finders arm still …
- research T-2120-review: Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect. [stale: plugin/lib/fmexam.py, plug…
## Decision
Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/36) with 0 false alarms, against the 0/108 baseline; it never fixes, so fix capabilities still need the production-model arms at the end; would change if: a later generation's finders run drops below 90/108 or reports a false alarm (then run the full arms for that capability, per the testing-cadence rule)
## Lessons
- a free deterministic arm turns a 0/108 baseline into a real number at zero tokens: run it first after any find capability ships
