---
id: T-0704
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T18:36:07Z
base: 32dc51b7c869df49c7f02dc2804600fb0d4c30be
base_tree: 0139406a4bf3aec79321232c2816c7bb01979074
verified: strong
---
# Frontier 04 — Zero-call bookkeeping and session lifecycle
## Raw request
> FEATURE: Frontier 04 — Zero-call bookkeeping and session lifecycle
> CONTEXT: Foreman state, close-out and handoffs take no model turns, and sessions are reborn from proven capsules instead of dragging stale context.
> CONTEXT: first slice: State inferred from events, one-call close-out returning one line, and a capsule format with a reproduce-the-failure acceptance check.
> CONTEXT: proof at close: Replay a day of tasks: model calls per task drop, and a reborn session continues a task to green from the capsule alone.
> CONTEXT: members (8, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Zero-round-trip bookkeeping; Zero-call bookkeeping: Foreman infers its own state, and close-out is one call that returns one verdict; No-poll waiting: background jobs wake the session, and the drive works on something else meanwhile; Clean-room tasks: every task starts in a fresh ~30k context, handed off by a cache-priced fork instead of a /compact; Rebirth: sessions die at every milestone or thrash and are reborn from a capsule proven sufficient by a quiz; Spawn by fork: every orchestrator is born as a prompt-cache fork of one primer session; Handoffs that must reproduce the failure before they're accepted; Incident timelines assembled mechanically; action items become tasks and rules
## Interpretation
First slice of Frontier 04: cut the bookkeeping turns measured over 14 days (460 tasks finished; 618 fm task evidence calls re-ran a command the session had just run; 135 fm task finish calls were refused and retried). A passing test run records itself as the current step's evidence; fm task finish names every gap in one refusal; a handoff packet carries the command that reproduces its failure and --check proves it still does.
## Assumptions (confidence)
## Acceptance criteria
- [x] A passing test run through a criterion's runner records the current step's evidence with no fm call; piped runs and red steps don't — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k StepEvidence`
- [x] fm task finish refuses once, naming missing lenses, docs, lesson and step evidence together — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinishGaps`
- [x] fm task packet carries a Reproduce section and --check accepts a handoff only while its failure still reproduces — verify with `python3 plugin/tests/run.py -p test_bookkeeping.py -k Reproduce`
## Non-goals
## Approach (options → choice → why)
Step evidence: (a) only a step's own exact verify command — steps rarely have one; (b) a passing command run through the same runner as a criterion's verify command or a project gate (python3 plugin/tests/run.py, npm test, cargo test…) — chosen: catches the -k variants actually run, still project-specific; (c) anything that looks like a test runner — records greps and installs; (d) a marker in the reply — still tokens, brittle. Piped or ;-chained commands are skipped (their exit status isn't the test's), as are steps about failing/red/reproducing. Finish: pre-check lenses (REQUIRED_AUDITS), docs, lesson and step evidence before running anything and raise once with all of them. Capsule: packet gains a Reproduce section from the newest failing fm-run command; --check reruns it: still failing = accepted, passing = stale handoff (exit 1). Deferred to later slices: state inferred from all events, no-poll waiting, clean-room fork handoffs, rebirth quiz.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] step evidence from passing runs (fmhooks)
3. [x] finish names every gap at once (fmcli)
4. [x] reproduce capsule: packet Reproduce + --check (fmcli)
5. [x] measure, CHANGELOG, full suite
## Resume here
## Docs impact
CHANGELOG; fm task packet --check help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py` → ✗ exit 1 · Ran 4 tests in 1.1s (3 classes, 16 at a time; slowest: StepEvidence 1s, FinishGaps 1s, Reproduce 0s) / FAILED (3 classes) [ran] [tree ed4db709fa75] (2026-10-09T18:31:30Z)
- (step 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -k StepEvidence` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: StepEvidence 1s) / OK [ran] [tree 65f1adbed856] (2026-10-09T18:32:51Z)
- (step 3) `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinishGaps` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: FinishGaps 1s) / OK [ran] [tree 65f1adbed856] (2026-10-09T18:32:52Z)
- (step 4) `python3 plugin/tests/run.py -p test_bookkeeping.py -k Reproduce` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Reproduce 0s) / OK [ran] [tree 04e3cc70eec8] (2026-10-09T18:33:07Z)
- (step 1) `python3 plugin/tests/run.py -p test_bookkeeping.py` → exit 0 · Ran 4 tests in 1.0s (3 classes, 16 at a time; slowest: StepEvidence 1s, FinishGaps 1s, Reproduce 0s) / OK [ran] [tree 04e3cc70eec8] (2026-10-09T18:33:08Z)
- (step 5) `python3 plugin/tests/run.py` → exit 0 · Ran 1132 tests in 56.7s (317 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree ed9bd32e5ae5] (2026-10-09T18:36:04Z)
- (ac 1) `python3 plugin/tests/run.py -p test_bookkeeping.py -k StepEvidence` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: StepEvidence 1s) / OK [ran] [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
- (ac 2) `python3 plugin/tests/run.py -p test_bookkeeping.py -k FinishGaps` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: FinishGaps 1s) / OK [ran] [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
- (ac 3) `python3 plugin/tests/run.py -p test_bookkeeping.py -k Reproduce` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Reproduce 0s) / OK [ran] [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
- (audit intent) `self review of the diff against the three criteria and the hook's hot path` → the first slice's three parts shipped (inferred step evidence, one-call close-out refusal, reproduce-checked capsule); no-poll waiting, clean-room forks and rebirth stay for later slices [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
- (audit edge) `self review of the diff against the three criteria and the hook's hot path` → a piped or ;-chained run, a red/reproduce step, a step already evidenced and an unknown runner record nothing; a failing run never auto-records; finish with no lenses at all on M now lists both audit groups instead of the old one-line hint [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
- (audit adversary) `self review of the diff against the three criteria and the hook's hot path` → auto evidence only fires on a real passing exit of a runner the task or project already declared, so a model can't mint evidence with echo; a crafted 'cd x && echo' is rejected by the && check after the cd strip [tree ed9bd32e5ae5] (2026-10-09T18:36:06Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T18:31:06Z focused
- 2026-10-09T18:36:06Z done
- 2026-10-09T18:36:07Z committed bbb2da3 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0703 [FEATURE M, done, 4 steps] Frontier 03 — Model routing, effort and cache economics — lesson: Context per turn, not output, drives spend here: thresholds for compa…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-09-26: Order after T-0016: T-0022 and T-0023 (user requests, explore items: take the recommendation after self-critique in full autonomy), then T-0018's ro…
- similar finished tasks took 3–4 steps
## Lessons
- Bookkeeping turns are measurable from transcripts: count fm calls that repeat the previous command or follow a refusal, and remove the cause rather than the call
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
