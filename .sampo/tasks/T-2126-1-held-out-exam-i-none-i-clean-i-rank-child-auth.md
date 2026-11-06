---
id: T-2126
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:48Z
updated: 2026-10-30T09:41:00Z
base: 6a4e7c18c695ab17284b76e1b6cfdc5b1d3d175e
base_tree: c92ba2d07975a56ff32c7ffc9caf9672601ba42e
plan0_at: 2026-10-30T09:20:46Z
plan0_scope: []
verified: strong
---
# #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7)
## Raw request
> #1 held-out exam: I-none, I-clean, I-rank child-authored kinds; finders, foreman and plain arms (Mission 3 brief 7)
## Interpretation
The #1 exam (gen-0 §2 Initiative) needs three no-request kinds: I-none (mixed defects, no request), I-clean (nothing planted; graded on 0 false alarms) and I-rank (defects of different severity; graded on the order they're named). Per standing rule 5 the scored ones are child-authored; template ones are fixtures.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen --author child makes I-none/I-clean/I-rank with a held-out third and the oracle closes each — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Complete version: KINDS gains clean and rank; CHILD_KINDS gains none and rank (the child plants one bug or vuln, the template adds untested + docs beside it, request empty); key.rank tiers [[vuln,bug],[rest]] graded by a new rank_keyed/rank_hit pair in _closed; untested moves off clamp when the child picked clamp so no finding matches two defects; empty closes only clean; oracle closes all.
A (chosen): one child plant + template extras — reuses the single-plant author, check and oracle paths, ~25 lines.
B: child returns a list of 3-4 plants — new reply schema, multi-function render, more drop risk; rejected for now (ponytail ceiling noted; revisit if child none proves too easy).
C: a separate initiative exam module — duplicates render/grade; rejected.
D: grade rank by a numeric severity field the arm sends — trusts the arm's own labels; rejected: order of findings is what scout and the pipeline act on.
## Risks and rollback
Old runs' keys lack rank: grading treats a missing rank as unranked (rank_keyed 0). Undo: git revert of the commit.
## Execution prompt
## Steps
1. [x] CHILD_KINDS none/clean/rank + grading
2. [x] run the three arms on the held-out third
## Resume here
<!-- auto -->
- 2026-10-30T09:29:00Z step 2/2: run the three arms on the held-out third
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/lib/fmcli.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmexam.py
## Docs impact
MASTER.md fmexam entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_find` → exit 0 · Ran 38 tests in 20.1s (19 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 43d0ec670737] (2026-10-30T09:25:22Z)
- (audit intent) `AC re-read vs diff: gen --author child makes none/clean/rank, held-out third via draw (n+1)//3, oracle closes all 9 of s31-006` → met; plan divergence (1 child bug + template untested/docs) recorded in the brief [tree ad55a3746c25] (2026-10-30T09:33:35Z)
- (audit adversary) `fm-reviewer pass + child text path: plant says/request go through c.plain + c.fit; child code runs with credentials stripped as before` → no new trust boundary; review findings fixed (genesis reshuffle) or captured (T-2131) [tree ad55a3746c25] (2026-10-30T09:33:35Z)
- (audit edge) `rank with one defect missed, vuln named last, one finding matching two tiers; old keys with no rank; planted clamp vs untested gap` → missed/last fail (tested); tie fails strict (documented); keys without rank grade as before; gap moves to label [tree ad55a3746c25] (2026-10-30T09:33:35Z)
- (audit operator) `summary row shows 'N/M ranked'; held-out run s31-006 plain arm: 2/9 closed, 6/18 found, 6 false alarms, $1.17` → an unranked close is now visible in the score row [tree ad55a3746c25] (2026-10-30T09:33:35Z)
- (audit maintainer) `KINDS growth no longer moves genesis G-scenario defects (frozen GEN_DEFECTS, pinned test); test_genesis caps pinned to GEN_DEFECTS` → adding a kind later is safe for #13's exam [tree ad55a3746c25] (2026-10-30T09:33:35Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 22 tests in 19.8s (10 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree ad55a3746c25] (2026-10-30T09:34:10Z)
- (step 2) `fm exam grade s31-006` → exit 0 · oracle s31-006: 18/18 found, 0 false alarms, 18/18 fixed, 6/6 test-first, 3/3 ranked, held out 18/18 found [ran] [tree ad55a3746c25] (2026-10-30T09:35:40Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 22 tests in 19.5s (10 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / OK [ran] [tree ad55a3746c25] (2026-10-30T09:38:06Z)
- (audit edge) `one fm-reviewer pass (3 findings: genesis defect reshuffle fixed test-first, rank summary part fixed, strict tie documented; prompt wording captured T-2131); held-out arms run on s31-006` → rank missed/last/tie and old keys without rank all tested or documented [tree ad55a3746c25] (2026-10-30T09:38:06Z)
- (audit adversary) `one fm-reviewer pass (3 findings: genesis defect reshuffle fixed test-first, rank summary part fixed, strict tie documented; prompt wording captured T-2131); held-out arms run on s31-006` → no new trust boundary; child text plain+fit [tree ad55a3746c25] (2026-10-30T09:38:06Z)
## Log
- 2026-10-30T08:06:48Z created
- 2026-10-30T09:20:46Z focused
- 2026-10-30T09:27:34Z found: real child replies trim only line 1's indent (rest at 4), so every python child plant dropped on IndentationError; _author now dedents the rest unless line 1 opens a block; stub replies in that shape now (red seen: 2 fails)
- 2026-10-30T09:33:17Z review: KINDS growth reshuffled fmgenesis._ask defects (h % len) -> frozen GEN_DEFECTS, pinned by test_g_scenario_defects_stay_put_when_exam_kinds_grow (red seen); summary() gains 'N/M ranked'; _in_order tie documented; genesis prompt wording captured
- 2026-10-30T09:35:39Z held-out arms on s31-006 (9: 3 none, 3 rank, 3 clean): oracle 9/9 closed, 18/18, 3/3 ranked; finders 3/9 closed (the clean ones), 16/18 found, 0 false alarms, 0/3 ranked; plain 2/9 closed, 6/18 found, 6 false alarms, $1.17; foreman 2/9 closed, 6/18 found, 7 false alarms, $1.71. Foreman adds nothing over plain on initiative with no request: the gap T-2122..T-2125 target
- 2026-10-30T09:38:33Z done
- 2026-10-30T09:38:35Z committed fafad9f5 (7 files)
- 2026-10-30T09:38:42Z guard authorization added: publish
- 2026-10-30T09:41:00Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2079 [FEATURE L, done, 6 steps] fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl — lesson: A claud…
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
## Why not caught
no test pinned a G-scenario id to its defect, so growing KINDS passed every test
## Lessons
- a module-level tuple used as a hash modulus (fmexam.KINDS in fmgenesis._ask) silently reshuffles every id when it grows; freeze the tuple the hash reads
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
