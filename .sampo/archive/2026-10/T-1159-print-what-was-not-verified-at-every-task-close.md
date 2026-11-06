---
id: T-1159
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:10:16Z
base: 515ab34bf32535e08a8fb62f2091e9724ed96af8
base_tree: 148506ee07cb90add4ed6355a245361fbf09be97
plan0_at: 2026-10-16T10:48:14Z
plan0_scope: []
verified: strong
---
# Print what was not verified at every task close: criteria with no verify command, unchecke
## Raw request
> FEATURE: Print what was not verified at every task close: criteria with no verify command, unchecked claims, and checks that were skipped.
> DONE-WHEN: `fm task finish` on a task with one unchecked claim and one criterion lacking a verify command prints both under "Not verified", and prints none on a fully verified task
## Interpretation
Every fm task finish says plainly what it did not verify, so a close never looks stronger than it is: criteria whose evidence was typed (no command ran), claims recorded as unchecked or inferred, and checks that were skipped (e.g. --affected only, a gate left out). A fully verified close prints nothing extra.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish on a task with one unchecked claim and one typed-evidence criterion prints both under 'Not verified'; a fully verified close prints no such block — verify with `python3 plugin/tests/run.py test_not_verified`
## Non-goals
## Approach (options → choice → why)
Options: (a) a 'Not verified:' block in finish's own output, built from the brief's evidence lines and claims; (b) a line in fm gates; (c) only in fm pr. Choice: (a); why: the close is where the reader looks and finish already loads the evidence and claims. Keep it to at most 5 lines with a count for the rest.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_not_verified.py): unchecked claim and typed criterion listed; fully verified prints none; --json carries the list
2. [x] The Not verified block in fm task finish's output
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_not_verified` → ✗ exit 1 · Ran 3 tests in 4.6s (1 classes, 16 at a time; slowest: NotVerified 4s) / FAILED (1 classes) [ran] [tree 7e20b292694a] (2026-10-16T10:48:45Z)
- (step 2) `python3 plugin/tests/run.py test_not_verified` → ✗ exit 1 · Ran 3 tests in 6.7s (1 classes, 16 at a time; slowest: NotVerified 6s) / FAILED (1 classes) [ran] [tree 48ff00beb794] (2026-10-16T10:49:24Z)
- (step 2) `python3 plugin/tests/run.py test_not_verified` → exit 0 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: NotVerified 4s) / OK [ran] [tree fdf2724c71ce] (2026-10-16T10:51:51Z)
- (step 2) `python3 plugin/tests/run.py test_not_verified test_cli test_bookkeeping` → exit 0 · Ran 118 tests in 47.4s (37 classes, 16 at a time; slowest: TaskLifecycle 47s, StateViews 18s, AuditPrep 13s) / OK [ran] [tree 349fe4aa750e] (2026-10-16T10:59:31Z)
- (ac 1) `python3 plugin/tests/run.py test_not_verified test_cli test_bookkeeping` → exit 0 · Ran 118 tests in 23.0s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 10s, AuditPrep 8s) / OK [ran] [tree 769d9a834ebc] (2026-10-16T11:08:23Z)
- (ac 1) `python3 plugin/tests/run.py test_not_verified` → exit 0 · Ran 4 tests in 4.1s (1 classes, 16 at a time; slowest: NotVerified 4s) / OK [ran] [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
- (audit intent) `reviewer: one fm-reviewer pass found the new block duplicated Check by hand, a false skipped line, and cap order; builder merged both into one Not verified block (check_by_hand JSON key kept), set the waiver flag where it is logged, and ordered claims first` → a close never looks stronger than it is [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
- (audit adversary) `reviewer: one fm-reviewer pass found the new block duplicated Check by hand, a false skipped line, and cap order; builder merged both into one Not verified block (check_by_hand JSON key kept), set the waiver flag where it is logged, and ordered claims first` → claim text is already redacted and cut to 90 chars by parse_claims; nothing unbounded printed [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
- (audit edge) `reviewer: one fm-reviewer pass found the new block duplicated Check by hand, a false skipped line, and cap order; builder merged both into one Not verified block (check_by_hand JSON key kept), set the waiver flag where it is logged, and ordered claims first` → --skip-affected with nothing to waive prints nothing; a fully verified close prints no block [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
- (audit operator) `reviewer: one fm-reviewer pass found the new block duplicated Check by hand, a false skipped line, and cap order; builder merged both into one Not verified block (check_by_hand JSON key kept), set the waiver flag where it is logged, and ordered claims first` → one block, capped at 5 lines with a count [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found the new block duplicated Check by hand, a false skipped line, and cap order; builder merged both into one Not verified block (check_by_hand JSON key kept), set the waiver flag where it is logged, and ordered claims first` → _close_unverified removed; by_hand is the single source [tree 38a44f64b3aa] (2026-10-16T11:08:38Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T10:47:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1159.builder.md
- 2026-10-16T10:48:14Z focused
- 2026-10-16T11:07:55Z merged worktree-agent-ad8a506f9587956cb (4 file(s))
- 2026-10-16T11:07:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad8a506f9587956cb
- 2026-10-16T11:07:59Z focused
- 2026-10-16T11:08:33Z scope: CHANGELOG.md; test_cli and test_bookkeeping updated for the merged block
- 2026-10-16T11:10:16Z done
- 2026-10-16T11:10:16Z committed 5705a02 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Lessons
- before adding a report block, grep the close output for one that lists the same thing
## Plan gaps
- failed first: step 1 Failing tests (test_not_verified.py): unchecked claim and typed criterion listed; fully verified pr…
- failed first: step 2 The Not verified block in fm task finish's output
## Files touched
- plugin/tests/test_not_verified.py
- plugin/lib/fmcli.py
- plugin/tests/test_cli.py
- plugin/tests/test_bookkeeping.py
- CHANGELOG.md
