---
id: T-1517
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/lib/fmevolve.py, plugin/lib/fmreplay.py, plugin/tests/fixtures/guard_allow.jsonl, plugin/tests/test_guard_cases.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:43Z
updated: 2026-10-22T20:30:49Z
base: 2c7e617b0bf216dd46099b055e8d97090a2457c5
base_tree: dc65d5eb35c0e108a65496cbc21ac3e6e63a912c
plan0_at: 2026-10-22T20:04:49Z
plan0_scope: [plugin/lib/fmguard.py, plugin/lib/fmevolve.py, plugin/lib/fmreplay.py, plugin/tests/fixtures/guard_allow.jsonl, plugin/tests/test_guard_cases.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 22): safety ratchet: an allow-corpus of everyday comman
## Raw request
> Brainstorm T-1479 round 2 (cluster 22): safety ratchet: an allow-corpus of everyday commands the guard must pass, the guard's own files locked against fm evolve, and a pass/fail/unable result for checks
## Interpretation
Safety ratchet: an allow-corpus of everyday commands the guard must pass (false-positive guard), the guard's own files locked against fm evolve (it may never propose an edit there), and checks return pass, fail or unable (a check that couldn't run is never a pass).
## Assumptions (confidence)
## Acceptance criteria
- [x] the allow-corpus replays green, fm evolve refuses a guard path, and an unrunnable check reports unable — verify with `cd plugin/tests && python3 -m unittest test_guard_cases.AllowCorpus`
## Non-goals
## Approach (options → choice → why)
Options: rely on the block corpus alone; chosen: a second labelled corpus (should: allow) replayed with the existing one, an fm evolve refusal for guard paths, and an 'unable' result kind.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] allow-corpus
3. [x] evolve lock
4. [x] unable result
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus` → ✗ exit 1 · Ran 7 tests in 0.3s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / FAILED (1 classes) [ran] [tree f2277e976cd1] (2026-10-22T20:12:26Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_every_everyday_command_passes -k test_guard_cases.AllowCorpus.test_the_replay_holds_both_corpora -k test_guard_cases.AllowCorpus.test_a_label_contradicting_the_allow_corpus_is_refused_and_names_it` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / OK [ran] [tree 0017cb699008] (2026-10-22T20:15:36Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_evolve_never_revises_the_guards_own_files -k test_guard_cases.AllowCorpus.test_evolve_refuses_a_link_in_place_of_an_instruction_file -k test_evolve` → exit 0 · Ran 13 tests in 10.3s (5 classes, 16 at a time; slowest: Evolve 10s, Failures 0s, AllowCorpus 0s) / OK [ran] [tree 0017cb699008] (2026-10-22T20:15:50Z)
- (step 4) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_an_unrunnable_check_reports_unable -k test_guard_cases.AllowCorpus.test_the_replay_reports_unable_and_fails` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / OK [ran] [tree 0017cb699008] (2026-10-22T20:15:51Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus` → ✗ exit 1 · Ran 12 tests in 0.5s (1 classes, 16 at a time; slowest: AllowCorpus 0s) / FAILED (1 classes) [ran] [tree 3adbc5a7b106] (2026-10-22T20:25:23Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus -k test_safety_gate` → exit 0 · Ran 24 tests in 3.9s (3 classes, 16 at a time; slowest: SafetyGate 4s, ReleaseGate 2s, AllowCorpus 0s) / OK [ran] [tree 1cd17a56f6e5] (2026-10-22T20:28:31Z)
- (step 3) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus.test_evolve_never_revises_the_guards_own_files -k test_guard_cases.AllowCorpus.test_evolve_refuses_a_link_or_a_folder_in_place_of_an_instruction_file -k test_evolve` → exit 0 · Ran 13 tests in 11.1s (5 classes, 16 at a time; slowest: Evolve 11s, Failures 0s, AllowCorpus 0s) / OK [ran] [tree 1cd17a56f6e5] (2026-10-22T20:28:42Z)
- (step 4) `python3 plugin/tests/run.py -k test_guard_cases.AllowCorpus -k test_friction -k test_replay` → exit 0 · Ran 35 tests in 6.3s (8 classes, 16 at a time; slowest: Friction 6s, Replay 3s, UserPromptSubmit 1s) / OK [ran] [tree 1cd17a56f6e5] (2026-10-22T20:28:49Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_cases.AllowCorpus` → exit 0 · Ran 12 tests in 0.292s / OK [ran] [tree c82f9c9484cf] (2026-10-22T20:29:25Z)
- (step 1) `python3 plugin/tests/run.py test_guard_cases test_evolve test_guard_evasions test_safety_gate` → exit 0 · Ran 50 tests in 16.3s (9 classes, 16 at a time; slowest: Evolve 16s, SafetyGate 5s, ReleaseGate 3s) / OK [ran] [tree c82f9c9484cf] (2026-10-22T20:29:53Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_cases.AllowCorpus` → exit 0 · Ran 12 tests in 0.285s / OK [ran] [tree eb3df44e6415] (2026-10-22T20:30:20Z)
- (audit intent) `one fm-reviewer pass (adversary-weighted): 1 MEDIUM + 5 LOW fixed test-first in b83ceb49; the builder also found and closed a real hole: fm evolve could write a rewrite into fmguard.py through a symlinked SKILL.md` → allow-corpus green, evolve refuses guard paths, unrunnable checks report unable [tree eb3df44e6415] (2026-10-22T20:30:20Z)
- (audit adversary) `one fm-reviewer pass (adversary-weighted): 1 MEDIUM + 5 LOW fixed test-first in b83ceb49; the builder also found and closed a real hole: fm evolve could write a rewrite into fmguard.py through a symlinked SKILL.md` → evolve lock covers the guard, hooks, their tests and fixtures, and the replay/evolve/mutate/bench code; symlinked files and parents are refused before the rewrite runs; reads use the pinned sha; no guard rule changed [tree eb3df44e6415] (2026-10-22T20:30:20Z)
- (audit edge) `one fm-reviewer pass (adversary-weighted): 1 MEDIUM + 5 LOW fixed test-first in b83ceb49; the builder also found and closed a real hole: fm evolve could write a rewrite into fmguard.py through a symlinked SKILL.md` → unable is its own bucket in drift, score, cmd_replay and fmfriction; opposite labels for one command and folder count as broken, not dropped [tree eb3df44e6415] (2026-10-22T20:30:20Z)
- (audit maintainer) `one fm-reviewer pass (adversary-weighted): 1 MEDIUM + 5 LOW fixed test-first in b83ceb49; the builder also found and closed a real hole: fm evolve could write a rewrite into fmguard.py through a symlinked SKILL.md` → AllowCorpus and evolve tests red first; replay shows 0 drift [tree eb3df44e6415] (2026-10-22T20:30:20Z)
## Log
- 2026-10-22T17:36:43Z created
- 2026-10-22T17:56:10Z set scope=['plugin/lib/fmguard.py', 'plugin/lib/fmevolve.py', 'plugin/lib/fmreplay.py', 'plugin/tests/fixtures/guard_allow.jsonl', 'plugin/tests/test_guard_cases.py', 'CHANGELOG.md']
- 2026-10-22T20:04:21Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1517.builder.md
- 2026-10-22T20:04:48Z focused
- 2026-10-22T20:29:23Z merged worktree-agent-aa51474fac55e1481 (6 file(s))
- 2026-10-22T20:29:23Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa51474fac55e1481
- 2026-10-22T20:29:24Z focused
- 2026-10-22T20:30:19Z scope: fmfriction.py (unable in the digest), MASTER.md and the allow-corpus fixture; other files from other tasks' merges
- 2026-10-22T20:30:47Z done
- 2026-10-22T20:30:49Z committed 7426a253 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_evolve.py, plugin/tests/test_guard.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmevolve.py, plugin/lib/fmguard.py, plugin/lib/fmreplay.py, plugin/tests/fixtures/guard_allow.jsonl, plugin/tests/test_guard_cases.py; re-ground the plan against them before editing
## Why not caught
fm evolve checked the target path's text, not where it resolves
## Lessons
- A self-improvement loop needs its judge locked: anything that can edit instruction files must be unable to reach the guard by any path, symlinks included
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/tests/fixtures/guard_allow.jsonl
- plugin/lib/fmreplay.py
- plugin/lib/fmevolve.py
- MASTER.md
- plugin/lib/fmfriction.py
- CHANGELOG.md
