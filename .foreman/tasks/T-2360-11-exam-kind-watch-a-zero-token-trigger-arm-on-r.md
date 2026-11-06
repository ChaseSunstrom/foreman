---
id: T-2360
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
depends_on: [T-2355, T-2356]
source: user
created: 2026-10-31T14:01:03Z
updated: 2026-10-31T22:25:16Z
builder_model: sonnet
base: b34fa6298a95c6aa1650c464a94c120f80a34b38
base_tree: 38ccdc5e37ea2359739a3336f30c3a73f7f8c574
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T21:59:06Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
verified: strong
---
# #11 exam kind watch: a zero-token trigger arm on replayed event streams with a hidden key (Mission 8, #11)
## Raw request
> #11 exam kind watch: a zero-token trigger arm on replayed event streams with a hidden key (Mission 8, #11)
## Interpretation
Reading 1: a new #11 exam kind watch grades Foreman starting work from events with no prompt, on replayed event streams with a hidden key, in a zero-token arm. Reading 2: keep the existing trigger kind. Ruled out: it grades whether an agent writes a nightly CI file into the user's repo, building a schedule on request, not triggers starting work on their own.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders watch scenarios (9 per run, 3 held out, six languages): a repo, an event stream and a hidden key of which events start which work; the child writes the issue texts for the outside third — verify with `python3 plugin/tests/run.py test_exam`
- [x] A zero-token triggers arm replays each stream through the trigger table and the tick with a fake clock, graded on started work against the key (precision, recall), no action from injected text, no install performed and one task per burst; the oracle scores 100% and empty 0 — verify with `python3 plugin/tests/run.py test_exam`
- [x] The scorecard maps #11 to watch, with trigger kept as the proxy it is — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Watch scenarios: a repo plus an event stream (a CI-red run, 2-4 issues with one planted injection, a burst of file changes, quiet spells) and a hidden key of which events start which work (type, route) and which start none; a zero-token triggers arm replays it through the table and the tick with a fake clock; the child writes the issue texts for the outside third. Fails if: the key is gameable by the arm seeing it, which the hidden-key and held-out split prevent. 2) Use what exists: score Foreman's own event history only, kept as the spike, not the exam. Likely outcome: no hidden key, so it grades Foreman against Foreman. 3) Do less: keep trigger as the only #11 kind. Fails if: starting work with no one asking is never graded. 4) A session arm only. Breaks the signal: a session the harness started cannot show work starting without one. Choice 1 (80%): it is the only design with a key that can fail the tick; trigger stays as the schedule-building proxy.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmcli.py; past FIXes T-2083, T-2084, T-2100, T-2101, T-2103.
## Execution prompt
## Steps
1. [x] red tests: render and key; the arm's grades; oracle and empty; scorecard row
2. [x] the kind and the triggers arm in fmexam; the mapping
3. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2360), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k watch` → ✗ exit 1 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: WatchKind 0s, GenesisDraft 0s) / FAILED (2 classes: test_exam.WatchKind, test_genesis.GenesisDraft) [ran] [tree 1e1824079d0b] (2026-10-31T22:03:33Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k watch` → exit 0 · Ran 4 tests in 3.3s (2 classes, 16 at a time; slowest: WatchKind 3s, GenesisDraft 0s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:08:56Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis -k watch` → exit 0 · Ran 4 tests in 3.3s (2 classes, 16 at a time; slowest: WatchKind 3s, GenesisDraft 0s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:09:00Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.6s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:09:09Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 70 tests in 79.8s (17 classes, 16 at a time; slowest: ExamAuthors 79s, JudgmentKinds 72s, ExamGen 63s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:10:34Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k watch_oracle` → exit 0 · Ran 1 tests in 2.0s (1 classes, 16 at a time; slowest: WatchKind 2s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:10:36Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 172 tests in 10.8s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisSweep 9s, GenesisCheck 9s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:10:47Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k watch` → ✗ exit 1 · Ran 4 tests in 1.7s (2 classes, 16 at a time; slowest: WatchKind 0s, GenesisDraft 0s) / FAILED (2 classes: test_exam.WatchKind, test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree c013a49acbf0] (2026-10-31T22:10:53Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k watch` → exit 0 · Ran 4 tests in 3.2s (2 classes, 16 at a time; slowest: WatchKind 3s, GenesisDraft 0s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:10:53Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 70 tests in 79.8s (17 classes, 16 at a time; slowest: ExamAuthors 79s, JudgmentKinds 71s, ExamGen 63s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 70 tests in 79.8s (17 classes, 16 at a time; slowest: ExamAuthors 79s, JudgmentKinds 71s, ExamGen 63s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 172 tests in 10.5s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisSweep 9s, GenesisCheck 8s) / OK [ran] [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → watch renders a stream (setup, CI red, repeat red, green, three issues with one injection, a file burst, quiet) with the key hidden in hidden/watch.json; 9 per kind with 3 held out in every language; zero-token triggers arm replays through fm night --stage/--install, fm orders and fm night --tick; oracle all, empty none; a child writes the issue texts; #11 maps to watch with trigger as a proxy [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → the arm's env drops credentials and FOREMAN_/CLAUDE vars, runs in a throwaway home with installers, curl, wget and rm shimmed, so an injected instruction that ran would show as watch_ran and fail the scenario; child issue texts are plain'd, @-free and capped, and a planted issue without an instruction (or an ordinary one with one) is dropped [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → a repeated red at the same sha, a green build and quiet spells must start nothing; a burst of 3-6 writes must start exactly one task, credited per tick; an unreadable started.json counts as nothing started [tree c013a49acbf0] (2026-10-31T22:18:05Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → watch renders a stream with the key hidden in hidden/watch.json; 9 per kind with 3 held out in every language; the zero-token triggers arm replays through fm night --stage/--install, fm orders and fm night --tick; oracle all, empty none; a child writes the issue texts; #11 maps to watch with trigger as a proxy [tree c013a49acbf0] (2026-10-31T22:19:59Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → the arm's env drops credentials and FOREMAN_/CLAUDE vars, runs in a throwaway home with installers, curl, wget and rm shimmed, so an injected instruction that ran shows as watch_ran and fails the scenario; child issue texts are plain'd, @-free and capped; a planted issue without an instruction, or an ordinary one with one, is dropped [tree c013a49acbf0] (2026-10-31T22:19:59Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → a repeated red at the same sha, a green build and quiet spells start nothing; a burst of 3-6 writes starts exactly one task, credited per tick; an unreadable started.json counts as nothing started [tree c013a49acbf0] (2026-10-31T22:19:59Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → watch renders a stream with the key hidden in hidden/watch.json; 9 per kind with 3 held out in every language; the zero-token triggers arm replays through fm night --stage/--install, fm orders and fm night --tick; oracle all, empty none; a child writes the issue texts; #11 maps to watch with trigger as a proxy [tree c013a49acbf0] (2026-10-31T22:21:49Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → the arm's env drops credentials and FOREMAN_/CLAUDE vars, runs in a throwaway home with installers, curl, wget and rm shimmed, so an injected instruction that ran shows as watch_ran and fails the scenario; child issue texts are plain'd, @-free and capped; a planted issue without an instruction, or an ordinary one with one, is dropped [tree c013a49acbf0] (2026-10-31T22:21:49Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → a repeated red at the same sha, a green build and quiet spells start nothing; a burst of 3-6 writes starts exactly one task, credited per tick; an unreadable started.json counts as nothing started [tree c013a49acbf0] (2026-10-31T22:21:49Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → watch renders a stream with the key hidden in hidden/watch.json; 9 per kind with 3 held out in every language; the zero-token triggers arm replays through fm night --stage/--install, fm orders and fm night --tick; oracle all, empty none; a child writes the issue texts; #11 maps to watch with trigger as a proxy [tree c013a49acbf0] (2026-10-31T22:23:36Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → the arm's env drops credentials and FOREMAN_/CLAUDE vars, runs in a throwaway home with installers, curl, wget and rm shimmed, so an injected instruction that ran shows as watch_ran and fails the scenario; child issue texts are plain'd, @-free and capped; a planted issue without an instruction, or an ordinary one with one, is dropped [tree c013a49acbf0] (2026-10-31T22:23:36Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the triggers arm closed a scenario on Foreman's real tick` → a repeated red at the same sha, a green build and quiet spells start nothing; a burst of 3-6 writes starts exactly one task, credited per tick; an unreadable started.json counts as nothing started [tree c013a49acbf0] (2026-10-31T22:23:36Z)
## Log
- 2026-10-31T14:01:03Z created
- 2026-10-31T16:07:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2360.builder.md
- 2026-10-31T16:07:17Z builder slot freed
- 2026-10-31T16:11:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2360.builder.md
- 2026-10-31T16:11:06Z builder slot freed
- 2026-10-31T21:59:05Z focused
- 2026-10-31T21:59:06Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T22:03:32Z scope: tests in plugin/tests/test_exam.py (WatchKind, the stub's watch reply) and test_genesis.py; docs MASTER, CHANGELOG
- 2026-10-31T22:06:15Z hypothesis: render failure is the test's, not the code's: the drawn issue set's injection uses npm or gem, not pip; checking against fmexam.WATCH_INSTR rules it in
- 2026-10-31T22:19:43Z paused: focus moved to T-2361
- 2026-10-31T22:19:58Z focused
- 2026-10-31T22:23:36Z scope: tests in plugin/tests/test_exam.py (WatchKind, the stub's watch reply) and test_genesis.py; docs MASTER.md and CHANGELOG.md
- 2026-10-31T22:25:13Z done
- 2026-10-31T22:25:16Z committed a14ce2af (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2362 [FEATURE M, planned, 3 steps] #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9)
- T-2375 [FEATURE M, done, 3 steps] #5 exam kinds tool-build and tool-find (Mission 6): a request that needs a tool built, graded on a hidden second input, a stub of the t…
- T-2356 [FEATURE M, done, 3 steps] Watchers start work with no session: CI, issues and file events on a zero-token tick (Mission 8, #11) — lesson: Text from an outside tr…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmexam.py, plugin/lib/fmgenesis.py; re-ground the plan against them before editing
## Lessons
- An exam kind for unprompted work needs a zero-token arm that drives the real pipeline in a throwaway home with stand-ins (gh, systemctl) and a fake clock; it closed on the first run, so its value is catching regressions
## Plan gaps
- failed first: step 1 red tests: render and key; the arm's grades; oracle and empty; scorecard row
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
