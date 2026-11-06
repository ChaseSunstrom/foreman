---
id: T-1120
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-10-16T06:00:51Z
updated: 2026-10-16T06:44:12Z
base: d76f0c2c62c8d0426ca998ae1311150fd0d83ca2
base_tree: 7fb18416df59ab2a7773d63cffd2d7505e374c97
verified: strong
---
# Guard tests for the six rules fm bench guard --mutate found untested (T-1066 real run): pi
## Raw request
> Guard tests for the six rules fm bench guard --mutate found untested (T-1066 real run): pipe-shell 'eval of a downloaded script' (fmguard.py ~2324), self-authorize fm posture lite / fm pause off / fm approve-reads on / fm rule rm (~2393-2403), rm-outside recursive rm with targets from stdin (~2780); then rerun --mutate to 0 survivors
## Interpretation
fm bench guard --mutate (T-1066) dropped each of these rule sites and the guard's tests still passed, so nothing proves them: pipe-shell 'eval of a downloaded script' (fmguard.py ~2324), self-authorize fm posture lite, fm pause off, fm approve-reads on, fm rule rm (~2393-2403), rm-outside recursive rm with targets from stdin (~2780). Add table rows to plugin/tests/test_guard.py (GuardAgainstBash-style run_table with the expected category) for each, plus the near-miss allowed forms (fm posture, fm pause on, fm rule list, xargs rm without -r on a file list), so dropping any of the six fails a test.
## Assumptions (confidence)
## Acceptance criteria
- [x] Each of the six rule sites has a test row asserting its category, and the allowed near-misses stay allowed — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Add the rows; temporarily drop each site by hand in a scratch copy (or with fm bench guard --mutate --only CATEGORY once T-1066 lands) to see each new row fail
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 108 tests in 7.1s (46 classes, 16 at a time; slowest: GuardAgainstBash 7s, Hook 2s, RuleIds 1s) / OK [ran] [tree 2717631a7818] (2026-10-16T06:13:35Z)
- (ac 1) `fm bench guard --mutate --only self-authorize --max 20` → exit 0 · Guard mutation (drop): 5 of 5 mutants, 5 killed, 0 survived / not mutated (no rule site found): confirm [ran] [tree 35ff054df9b9] (2026-10-16T06:43:38Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 110 tests in 5.0s (46 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, RuleIds 0s) / OK [ran] [tree c25a0a359336] (2026-10-16T06:43:44Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1082/T-1048); review notes folded (no allow row that pins a gap, exact phrases); verified by mutation on the merged tree: system 19/19, rm-outside 4/4, self-authorize 5/5, pipe-shell 4/4 killed` → each row asserts category and the rule's own detail phrase, so another rule of the same category can't mask a dropped site; the two gaps a row would have pinned (stdin-fed plain rm, eval of printed text) went to T-1123 instead of an allow row [tree c25a0a359336] (2026-10-16T06:43:44Z)
- (audit self) `review: one fm-reviewer pass (combined with T-1082/T-1048); review notes folded (no allow row that pins a gap, exact phrases); verified by mutation on the merged tree: system 19/19, rm-outside 4/4, self-authorize 5/5, pipe-shell 4/4 killed` → no findings [tree c25a0a359336] (2026-10-16T06:43:44Z)
## Log
- 2026-10-16T06:00:51Z created
- 2026-10-16T06:12:44Z set scope=['plugin/tests/test_guard.py']
- 2026-10-16T06:12:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1120.builder.md
- 2026-10-16T06:12:51Z focused
- 2026-10-16T06:36:52Z merged worktree-agent-a391b828e646bfa9c (1 file(s))
- 2026-10-16T06:36:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a391b828e646bfa9c
- 2026-10-16T06:36:52Z focused
- 2026-10-16T06:43:39Z scope: CHANGELOG.md — release note
- 2026-10-16T06:44:11Z done
- 2026-10-16T06:44:12Z committed 8b544f6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- T-0581 [SECURITY M, done, 2 steps] Guard: a download piped into a ( group ) is still piped, with a space or a line break before the paren — lesson: a subshell paren afte…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Lessons
- Pin a rule's test to its own message, not just its category, or a sibling rule keeps the mutant alive
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
