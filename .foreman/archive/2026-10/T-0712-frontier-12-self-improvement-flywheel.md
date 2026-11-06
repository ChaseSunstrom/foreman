---
id: T-0712
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T19:28:17Z
base: b67b271e43765ca3c68a7a110828843c834e130f
base_tree: 974365bcdbb9eca83e2bba0e714336e7cb4d5e33
verified: strong
---
# Frontier 12 — Self-improvement flywheel
## Raw request
> FEATURE: Frontier 12 — Self-improvement flywheel
> CONTEXT: Foreman measures its own burden, tests changes on replays and ships proven improvements and detectors overnight.
> CONTEXT: first slice: Burden meter plus flight-recorder replay set that scores a candidate change.
> CONTEXT: proof at close: One overnight run produces a candidate that beats baseline on replays and merges with one approval.
> CONTEXT: members (20, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Rewind and re-decide: real failure moments become one-turn counterfactual tests; Burden meter: Foreman's own objective, measured on real sessions and attributed to each of its changes; Darwin archive: open-ended evolution of Foreman behind a multi-fidelity proof cascade; Flight recorder: every real hook decision becomes a free, labelled regression case; Live self-experiments: Foreman runs randomized trials of its own behaviour on real work; Corrections become backtested detectors that fire before the user has to say it; Proof-carrying self-changes with warranties checked on real sessions and revert proposals; Guard repair synthesizer: false blocks fixed overnight with a no-new-bypass proof; Improving the improver: a yield-ranked portfolio of improvement engines that evolves its own prompts; Overnight flywheel: wake up to proven Foreman improvements and merge each with one click; Co-evolving benchmark: forged micro-tasks that live only while they tell variants apart; Treadmill detector: know when to stop patching and redesign; Night school: every past mistake becomes a permanent test, and Foreman rewrites its own skills, hooks and agents overnight against them; Lessons compile to code: memory stops being prose the model must read and becomes checks that run; Corrections become enforced code rules, backtested on history; Agent foundry: the agent roster is mined from real delegations, benched, trained on verdicts and retired; Prosecutor court: an adversary with tools that wins only with a failing test the judge rules valid; Trajectory JIT: the agent's hot habits are compiled into deterministic tools, and the hook swaps them in when the habit starts; Compiled skills: repeated tool-call sequences mined from transcripts become zero-token macros, triggered by their first step; Foreman writes the project's scripts from what it keeps typing
## Interpretation
First slice of Frontier 12: Foreman measures its own burden and scores a candidate change before it ships. fm burden [--days N] reads the session transcripts: per session and per Foreman version (from session_start's plugin root), the share of turns spent only on Foreman bookkeeping, guard refusals, refused fm calls and the context Foreman's hooks injected per turn, the objective a self-change must lower. fm replay --candidate REF scores another version of the guard (a git ref) on the replay corpus of real past commands: verdicts that flip either way, the loosened ones listed for review. The overnight generation of candidates (fm night) needs model runs and waits for usage headroom.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm burden reports per session and per Foreman version the bookkeeping-only turn share, guard refusals, refused fm calls and injected context per turn — verify with `python3 plugin/tests/run.py -p test_flywheel.py -k Burden`
- [x] fm replay --candidate REF lists the corpus verdicts that flip between the working guard and the candidate's, loosened ones first — verify with `python3 plugin/tests/run.py -p test_flywheel.py -k Candidate`
## Non-goals
## Approach (options → choice → why)
Burden source: (a) the ledger — misses the turns themselves; (b) transcripts (as fm cost reads them) plus the inject log — chosen: turns, refusals and injected text are all there; (c) live counters in the hooks — only from now on. Version attribution: the plugin root each session_start logged (its version folder). Candidate scoring: (a) run the candidate's whole plugin in a sandbox — heavy; (b) load the candidate's fmguard.py from git show REF into a temp module and run the corpus through both — chosen: the guard is a pure function of command and context; other hook changes are scored by the burden meter after release. Deferred: Darwin archive, randomized self-experiments, detector synthesis.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fm burden
3. [x] fm replay --candidate
4. [x] measure on this machine, docs, CHANGELOG, full suite
## Resume here
## Docs impact
CHANGELOG; MASTER.md (fmcost burden, fmreplay --candidate)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_flywheel.py` → ✗ exit 1 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: Burden 0s, Candidate 0s) / FAILED (2 classes) [ran] [tree 955ff15e12cc] (2026-10-09T19:23:38Z)
- (step 2) `python3 plugin/tests/run.py -p test_flywheel.py -k Burden` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Burden 0s) / OK [ran] [tree b63ffba7b8e4] (2026-10-09T19:27:09Z)
- (step 3) `python3 plugin/tests/run.py -p test_flywheel.py -k Candidate` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Candidate 0s) / OK [ran] [tree b63ffba7b8e4] (2026-10-09T19:27:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_flywheel.py` → exit 0 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: Burden 0s, Candidate 0s) / OK [ran] [tree b63ffba7b8e4] (2026-10-09T19:27:10Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1156 tests in 59.8s (334 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree 93c0781f3511] (2026-10-09T19:28:10Z)
- (ac 1) `python3 plugin/tests/run.py -p test_flywheel.py -k Burden` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Burden 0s) / OK [ran] [tree 93c0781f3511] (2026-10-09T19:28:17Z)
- (ac 2) `python3 plugin/tests/run.py -p test_flywheel.py -k Candidate` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Candidate 0s) / OK [ran] [tree 93c0781f3511] (2026-10-09T19:28:17Z)
- (audit intent) `self review of fm burden, the candidate loader and scoring; real runs on this machine's 7 days of sessions and the 5000-command corpus` → the first slice asked for a burden meter and a replay set that scores a candidate change; both shipped and ran on real data; the overnight generator is a recorded decision for a window with usage headroom [tree 93c0781f3511] (2026-10-09T19:28:17Z)
- (audit adversary) `self review of fm burden, the candidate loader and scoring; real runs on this machine's 7 days of sessions and the 5000-command corpus` → a candidate is loaded as Python, so only a path the user names or a ref of Foreman's own repo; it runs in fm's process like the working guard and decides nothing live; a loosening candidate exits 1 so nothing gates on it by accident [tree 93c0781f3511] (2026-10-09T19:28:17Z)
- (audit edge) `self review of fm burden, the candidate loader and scoring; real runs on this machine's 7 days of sessions and the 5000-command corpus` → sessions without a session_start are 'unknown'; a dev install is 'working copy'; a message split over several transcript lines is one turn; only hook text naming Foreman counts as injected; Python snippets' escape warnings in the corpus are silenced [tree 93c0781f3511] (2026-10-09T19:28:17Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T19:19:53Z focused
- 2026-10-09T19:28:17Z done
- 2026-10-09T19:28:17Z committed 991f827 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0680 [FEATURE M, done, 4 steps] Milestone: Features — Self-improvement and learning — lesson: Measure what the harness itself injects: notes are tokens too, and a note…
- T-0706 [FEATURE M, done, 5 steps] Frontier 06 — Debugging intuition engine — lesson: Fault localisation inside a task: the change since the last green is the strongest p…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 4–5 steps
## Lessons
- Self-improvement needs an objective before candidates: measure the burden per version from transcripts, and score guard changes on the real command corpus, both free of model calls
## Files touched
- plugin/tests/test_flywheel.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
- MASTER.md
- .claude-plugin/marketplace.json
- plugin/.claude-plugin/plugin.json
