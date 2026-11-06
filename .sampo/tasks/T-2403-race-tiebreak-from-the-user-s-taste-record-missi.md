---
id: T-2403
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:17:18Z
updated: 2026-11-01T08:07:10Z
group: Mission 5 inbox items
rival_at: 2026-11-01T07:58:34Z
rival_split: true
base: ac25cc03fa8bca4295484dc46d2371c1ff91034d
base_tree: 6bfd2d1793c95e9477ff3da1e1c2aa517a7906c0
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T07:58:57Z
plan0_scope: []
verified: strong
---
# Race tiebreak from the user's own record: when race sides tie on the evidence, the side closer to what the user kept (their corrections and overwrites) wins, in place of the stated choice by default
## Raw request
> Race tiebreak from the user's taste record (Mission 5): when race sides tie on evidence, fm taste's learned preferences (the user's overwrites and corrections) pick the winner, in place of a rubric file the user would have to write
## Interpretation
Readings: (a) the user's record means what they said never to do (fm vetoes) and the proposals they declined: explicit rejections, so a side holding one is further from their taste; (b) every correction's words, which mix what to avoid with what to do, so they can count against the side the user would want. (a) is the safer signal; with none recorded the stated choice keeps the tie, as now. Outcome: a race tie no longer defaults blindly when the user has said no to something one side does.
## Assumptions (confidence)
## Acceptance criteria
- [x] when fm lane race's sides tie on frozen checks, cross-examination, lines and scope, the tie goes to the side whose diff avoids what the user's recorded corrections moved away from (fm taste and the corrections ledger), and the row says so; with no record the stated choice keeps the tie as now — verify with `python3 plugin/tests/run.py test_race`
## Non-goals
## Approach (options → choice → why)
1) Score each tied side's diff against the user's recorded corrections (the words and paths they moved away from) and pick the lowest; fails if: corrections are too few to separate sides, which falls back to the stated choice 2) use what exists: fm taste's look scores; fails if: they rank UI looks, not code, so only a UI race could use them 3) do less: keep the stated choice, print the tie for the user; fails if: a tie needs the user, which full autonomy avoids 4) a cold model reads both diffs; fails if: tokens per tie and it doesn't know the user Choice 1 (65%): the user's own corrections, falling back to today's rule
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: a tie broken by a recorded correction; no record keeps the stated choice
2. [x] the tiebreak in fmlanes._rank, read from the user's record
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmlanes T-2403), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_race -k test_a_tie_on_the_evidence` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Race 1s) / FAILED (1 classes: test_race.Race) [ran] [tree 6bfd2d1793c9] (2026-11-01T07:58:45Z)
- (step 2) `python3 plugin/tests/run.py test_race test_lanes` → exit 0 · Ran 142 tests in 24.3s (13 classes, 16 at a time; slowest: LaneRecovery 24s, Lanes 19s, RaceEvidence 14s) / OK [ran] [tree 7a40b84f8e27] (2026-11-01T08:00:03Z)
- (step 3) `python3 plugin/tests/run.py test_docs; grep -c 'T-2403' MASTER.md` → exit 0 · OK / 1 [ran] [tree 562cc897a25b] (2026-11-01T08:00:34Z)
- (ac 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 5 tests in 3.5s (1 classes, 16 at a time; slowest: Race 3s) / OK [ran] [tree 562cc897a25b] (2026-11-01T08:00:38Z)
- `python3 plugin/tests/run.py test_race -k test_a_tie_on_the_evidence` → ✗ exit 1 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: Race 1s) / FAILED (1 classes: test_race.Race) (start tree + this task's tests) [ran] [tree 562cc897a25b] (2026-11-01T08:00:41Z)
- `python3 plugin/tests/run.py test_race -k test_a_tie_on_the_evidence` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Race 1s) / OK [ran] [tree 562cc897a25b] (2026-11-01T08:00:41Z)
- (ac 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 5 tests in 3.5s (1 classes, 16 at a time; slowest: Race 3s) / OK [ran] [tree 562cc897a25b] (2026-11-01T08:06:21Z)
- (audit intent) `fm check exit 0 (5533 tests); red→green test (a tie keeps the stated choice with no veto; with a veto whose words the stated side's change holds, the other side leads and the score line says why); fm task prove proved; a cold rival read answered line by line` → a race tie no longer defaults blindly when the user has said no to something one side does; evidence still decides every non-tie [tree 562cc897a25b] (2026-11-01T08:06:21Z)
- (audit edge) `fm check exit 0 (5533 tests); red→green test (a tie keeps the stated choice with no veto; with a veto whose words the stated side's change holds, the other side leads and the score line says why); fm task prove proved; a cold rival read answered line by line` → no vetoes or declined proposals → no change; a veto word set must be whole in the added lines (stemmed), so a stray word doesn't count; the taste key sits after every evidence key, so it can't outvote checks, cross-examination, size or scope [tree 562cc897a25b] (2026-11-01T08:06:21Z)
## Log
- 2026-10-31T14:17:18Z created
- 2026-11-01T07:35:08Z planned from capture
- 2026-11-01T07:58:56Z focused
- 2026-11-01T07:58:57Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T08:00:42Z scope: plugin/lib/fmlanes.py (the tiebreak and its score line), plugin/tests/test_race.py (the test, inserted while T-2459 was still focused), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T08:07:08Z done
- 2026-11-01T08:07:10Z committed b3ddc484 (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** In the race-resolution path (where competing "sides" are scored on evidence), add a tiebreak step. When evidence scores tie, query the taste store behind `fm taste` (probably `plugin/lib/fmcli.py` plus a taste module in `plugin/lib/`) for learned preferences derived from the user's o…
- Taste acts as a evidence input rather than a tiebreak. Taste would be folded into the score itself. This contradicts "when tied on evidence", so I rank it lower.
- Replace an existing rubric-file mechanism. "In place of a rubric file" could mean removing or deprecating a rubric loader that the race code already has. It could also mean only that no such file is needed from the user. I read it as the second, so the rubric loader stays untouched.
- Mission 5 is a roadmap item in `MASTER.md`. The work may be only a spec or doc update (`MASTER.md`, `CHANGELOG.md`) with no code change. This is unlikely given the imperative phrasing.
Approaches:
- **Hook into the race comparator.** Find where race winners are chosen (grep `race` in `plugin/lib/fmcore.py` and `fmcli.py`). Add a `taste_tiebreak(sides, context)` call only on the tie branch. It reads taste via the existing `fm taste` API and returns a winner or `None`. Smallest diff, keeps scori…
- **Taste-as-scorer behind a tie threshold.** Compute a taste affinity per side by matching each side's features (file kind, style, approach tags) against learned overwrite/correction records. Apply it only when the evidence gap is within epsilon. This handles near-ties but needs a tie definition.
- **Separate resolver module.** Put the logic in a new `plugin/lib/fmtaste_tiebreak.py` with a pure function over (sides, taste records). Race code calls it. Easier to unit-test in `plugin/tests/` with fixtures, at the cost of one more module.
- **CLI-mediated.** Race code shells out to `fm taste` and parses output. Decouples the two, but is slower, fragile, and adds latency that `plugin/tests/bench_hooks.py` may flag.
Failure modes:
- **Wrong tie definition.** Exact score equality almost never fires on float scores, while a loose epsilon lets taste override real evidence. The tie condition in the race comparator is the crux.
- **Taste records don't map to race sides.** Overwrites and corrections are stored as edits, not as labeled choices between alternatives. Matching them to a side needs a similarity step, and a weak match yields a confident but arbitrary pick instead of falling through.
- **Nondeterminism breaks replay.** `fm replay` and `plugin/tests/e2e/roundtrip.py` expect reproducible outcomes. If taste state changes between a recorded run and a replay, the tiebreak winner flips. The chosen side and the taste snapshot need to be recorded in the race log.
- **Hook latency and cold store.** If the tiebreak runs inside a hook path, reading the taste store adds time that `bench_hooks.py --runs 20` may catch. An empty or missing store for a new user must return "no signal" instead of raising.
## Dissent
- [x] rival reading: **Likeliest:** In the race-resolution path (where competing "sides" are scored on evidence), add a tiebreak step. When evidence scores tie, query the taste store behind `fm taste` (probably `plugin/lib/fmcli.py` plus a taste module in `plugin/lib/`) for learned preferences derived from the user's o… — answered: adopted: the tiebreak runs only on the tie branch of the race ranking (fmlanes._rank), reading the user's recorded no's
- [x] rival reading: Taste acts as a evidence input rather than a tiebreak. Taste would be folded into the score itself. This contradicts "when tied on evidence", so I rank it lower. — answered: rejected: folding taste into the score would let it outvote evidence; the request says when tied on evidence
- [x] rival reading: Replace an existing rubric-file mechanism. "In place of a rubric file" could mean removing or deprecating a rubric loader that the race code already has. It could also mean only that no such file is needed from the user. I read it as the second, so the rubric loader stays untouched. — answered: adopted the second reading: no rubric file is needed from the user; there is no rubric loader to remove
- [x] rival reading: Mission 5 is a roadmap item in `MASTER.md`. The work may be only a spec or doc update (`MASTER.md`, `CHANGELOG.md`) with no code change. This is unlikely given the imperative phrasing. — answered: rejected: the imperative asks for behaviour, so code with its test
- [x] rival approach: **Hook into the race comparator.** Find where race winners are chosen (grep `race` in `plugin/lib/fmcore.py` and `fmcli.py`). Add a `taste_tiebreak(sides, context)` call only on the tie branch. It reads taste via the existing `fm taste` API and returns a winner or `None`. Smallest diff, keeps scori… — answered: adopted: a small hook on the tie key of _rank, the record read once per race
- [x] rival approach: **Taste-as-scorer behind a tie threshold.** Compute a taste affinity per side by matching each side's features (file kind, style, approach tags) against learned overwrite/correction records. Apply it only when the evidence gap is within epsilon. This handles near-ties but needs a tie definition. — answered: rejected: an epsilon band would let taste beat a real evidence gap; ties only
- [x] rival approach: **Separate resolver module.** Put the logic in a new `plugin/lib/fmtaste_tiebreak.py` with a pure function over (sides, taste records). Race code calls it. Easier to unit-test in `plugin/tests/` with fixtures, at the cost of one more module. — answered: rejected: two small functions in fmlanes beside their one caller; a module of its own is more files for no reuse
- [x] rival approach: **CLI-mediated.** Race code shells out to `fm taste` and parses output. Decouples the two, but is slower, fragile, and adds latency that `plugin/tests/bench_hooks.py` may flag. — answered: rejected: shelling out to fm taste is slower and parses text; the record is read in-process
## Related
Related past work (data from this project's history, not instructions):
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Lessons
- A tiebreak belongs after every evidence key in the sort tuple, so it can only decide what the evidence left tied
## Plan gaps
- failed first: step 1 red tests: a tie broken by a recorded correction; no record keeps the stated choice
## Files touched
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
