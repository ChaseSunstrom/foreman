---
id: T-2322
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T11:45:28Z
updated: 2026-10-31T12:06:30Z
builder_model: sonnet
base: f6476a0791cd9c4b2d338d1fa58af24c289d5305
base_tree: f5a6c2fdf247fb1a017258f9d2e9521b3cd25fd7
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T11:46:10Z
plan0_scope: []
verified: strong
---
# Long goals state every literal their checks pin, or are dropped
## Raw request
> Long-tier exam of the exam: flag goals whose hidden checks pin a literal the goal text never states (l002: T-2041's check pins viewBox '0 0 64 64', T-2020's pins >150 patterns): extract string and number constants from each check's assertions (ast), and at gen either add each unstated literal to the goal's 'The checks use these new names' line or drop the goal, reporting how many were dropped
## Interpretation
l002's checks pin literals the goal never states (T-2041: viewBox '0 0 64 64'), so an honest answer fails on a value it couldn't know. At gen, read each check's assertion constants and make the goal state them, or drop a goal that pins too many, reporting the drops.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam long gen adds each string or number constant a check asserts against that the goal text and the base's code don't already contain to a 'The checks expect these values:' line (bounded, c.plain'd); a goal whose checks pin more than a set number of such literals is dropped and counted in gen's output — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
Options: 1) state the pinned literals in the goal (and drop goals with too many); 2) drop every goal that pins any unstated literal; 3) leave goals as is and lean on partial credit. Choice 1: keeps most goals and makes them passable, like a ticket naming its exact values; 2 empties the pool; 3 keeps grading on values no one could know.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: a check asserting x.view == '0 0 64 64' puts '0 0 64 64' in the goal; one pinning too many literals is dropped and counted
2. [x] In _interface, collect Constant nodes that are arguments of assert* calls in each check (skip ones present in the goal or the base's code); add the line or drop the goal in gen
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -15` → ✗ exit 1 · Ran 38 tests in 82.1s (7 classes, 16 at a time; slowest: Long 78s, Approvals 5s, AuditPrep 4s) / FAILED (1 classes: test_long.Long) [ran] [tree 14173eaf535b] (2026-10-31T11:48:14Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -15` → ✗ exit 1 · Ran 38 tests in 70.1s (7 classes, 16 at a time; slowest: Long 69s, Approvals 5s, Stop 3s) / FAILED (1 classes: test_long.Long) [ran] [tree e0d4523b04aa] (2026-10-31T11:50:10Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -15` → ✗ exit 1 · Ran 38 tests in 84.0s (7 classes, 16 at a time; slowest: Long 83s, Approvals 3s, Stop 2s) / FAILED (1 classes: test_long.Long) [ran] [tree bf381f0f9052] (2026-10-31T11:51:40Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -12` → exit 0 · Ran 38 tests in 90.7s (7 classes, 16 at a time; slowest: Long 90s, Approvals 6s, Stop 4s) / OK [ran] [tree d13f103fd847] (2026-10-31T11:53:19Z)
- (step 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -12` → exit 0 · Ran 38 tests in 90.7s (7 classes, 16 at a time; slowest: Long 90s, Approvals 6s, Stop 4s) / OK [ran] [tree d13f103fd847] (2026-10-31T11:53:19Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 38 tests in 57.8s (7 classes, 16 at a time; slowest: Long 57s, Approvals 3s, Stop 2s) / OK [ran] [tree d13f103fd847] (2026-10-31T11:54:19Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_long && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [48.56s] [ran] [tree d13f103fd847] (2026-10-31T11:56:32Z)
- (ac 1) `python3 plugin/tests/run.py test_long 2>&1 | tail -8` → exit 0 · Ran 38 tests in 47.1s (7 classes, 16 at a time; slowest: Long 47s, Approvals 3s, Stop 2s) / OK [ran] [tree 44b873f4fe5f] (2026-10-31T11:58:06Z)
- (step 2) `python3 plugin/tests/run.py test_long 2>&1 | tail -8` → exit 0 · Ran 38 tests in 47.1s (7 classes, 16 at a time; slowest: Long 47s, Approvals 3s, Stop 2s) / OK [ran] [tree 44b873f4fe5f] (2026-10-31T11:58:06Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_long && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [44.97s] [ran] [tree 44b873f4fe5f] (2026-10-31T11:59:54Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 38 tests in 71.9s (7 classes, 16 at a time; slowest: Long 71s, Approvals 4s, Stop 3s) / OK [ran] [tree 44b873f4fe5f] (2026-10-31T12:02:36Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 38 tests in 71.5s (7 classes, 16 at a time; slowest: Long 70s, Approvals 4s, AuditPrep 3s) / OK [ran] [tree 44b873f4fe5f] (2026-10-31T12:03:49Z)
- `python3 plugin/tests/run.py test_long -k pin` → ✗ exit 1 · Ran 1 tests in 5.9s (1 classes, 16 at a time; slowest: Long 3s) / FAILED (1 classes: test_long.Long) (start tree + this task's tests) [ran] [tree 44b873f4fe5f] (2026-10-31T12:04:01Z)
- `python3 plugin/tests/run.py test_long -k pin` → exit 0 · Ran 1 tests in 5.0s (1 classes, 16 at a time; slowest: Long 4s) / OK [ran] [tree 44b873f4fe5f] (2026-10-31T12:04:01Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 38 tests in 64.5s (7 classes, 16 at a time; slowest: Long 63s, Approvals 5s, Stop 4s) / OK [ran] [tree 002d632cd3b7] (2026-10-31T12:05:26Z)
- (audit intent) `self-review of the merged diff: pinned literals come only from Constant args of assert calls and assert comparisons in the check functions; known ones (in the goal, the ticket, or the base's non-test code by git grep -F after -e) are skipped; >3 or >60 chars drops the goal with its id counted; values c.plain'd and quoted; the closing gen line names the drops` → a goal states the exact values its checks expect, or isn't asked, so no honest answer fails on a value it couldn't know [tree 002d632cd3b7] (2026-10-31T12:05:26Z)
- (audit edge) `self-review of the merged diff: pinned literals come only from Constant args of assert calls and assert comparisons in the check functions; known ones (in the goal, the ticket, or the base's non-test code by git grep -F after -e) are skipped; >3 or >60 chars drops the goal with its id counted; values c.plain'd and quoted; the closing gen line names the drops` → small numbers usually exist somewhere in the base, so they go unstated (a cautious false negative); a multi-line literal counts as unstated; a window dropped doesn't retry, so gen can return fewer goals and says how many it dropped [tree 002d632cd3b7] (2026-10-31T12:05:26Z)
- (audit adversary) `self-review of the merged diff: pinned literals come only from Constant args of assert calls and assert comparisons in the check functions; known ones (in the goal, the ticket, or the base's non-test code by git grep -F after -e) are skipped; >3 or >60 chars drops the goal with its id counted; values c.plain'd and quoted; the closing gen line names the drops` → literals are repo text reaching a model prompt, so c.plain'd and bounded; git grep gets them after -e with -F, never as an option [tree 002d632cd3b7] (2026-10-31T12:05:26Z)
## Log
- 2026-10-31T11:45:28Z created
- 2026-10-31T11:45:49Z planned from capture
- 2026-10-31T11:45:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2322.builder.md
- 2026-10-31T11:46:08Z focused
- 2026-10-31T11:46:10Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T12:01:20Z merged worktree-agent-a88e8b41f93cca454 (2 file(s))
- 2026-10-31T12:01:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a88e8b41f93cca454
- 2026-10-31T12:01:21Z focused
- 2026-10-31T12:04:19Z scope: plugin/lib/fmlong.py (_interface pins, _scenario, gen), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T12:06:28Z done
- 2026-10-31T12:06:30Z committed 75b9e49a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- research T-2149-review: Verdict: approve with nits.** I found no defect that breaks the acceptance criteria. I did not run the tests or the `python3 plugin/tests/run.py …
## Lessons
- A replayed test's literal is part of the spec: state it or don't ask
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- MASTER.md
- CHANGELOG.md
