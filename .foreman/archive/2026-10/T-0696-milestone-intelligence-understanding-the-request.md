---
id: T-0696
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:18Z
updated: 2026-10-09T21:10:07Z
batch: [T-0595, T-0601, T-0602, T-0621, T-0622]
base: 5a6d477b92824c3638ca79a72864b3ed62d698ec
base_tree: 514c817aaa50380f03648bdf8c60152b27baefcb
verified: strong
---
# Milestone: Intelligence — Understanding the request and the user
## Raw request
> T-0595: FEATURE: Split a message into its parts (I001, value 4/5, effort S, risk low)
>   first version: Add a clause ledger at intake: every clause of a multi-part message maps to a captured task, an answer, or an explicit 'noted'; fm next flags unaccounted clauses. First step: a check in fm intake/capture that lists clauses with no task id.
>   what it is: Separates questions, orders and venting, accounts for every clause, and resolves 'it', 'those' and how much latitude a phrase grants.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0601: FEATURE: Turn steers into lasting rules (I003, value 4/5, effort M, risk low)
>   first version: Tag each steer standing or one-off, and for standing ones write a veto/rule candidate and sweep siblings. First step: classify steers in the ledger at close-out and propose fm vetoes entries via fm ask-style yes.
>   what it is: Generalises each steer into a principle, tells standing preferences from one-offs, and pins dictated numbers and stances.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0602: FEATURE: Learn from the user's reactions (I007, value 4/5, effort M, risk low)
>   first version: Label each finished task's outcome (kept, corrected, reverted, dropped) from the next user message and later commits, store in ledger, feed fm taste and bench. First step: outcome label on task finish plus revert/follow-up-edit detection from git.
>   what it is: Turns corrections, overrides, silence and follow-up edits into labelled feedback.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 10 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0621: FEATURE: Defend against misreading (I002, value 3/5, effort S, risk low)
>   first version: Extend fm oracle to also emit the worst plausible misreading and one intake probe per misreading class, saved in the brief. Reuses existing oracle child.
>   what it is: Generates likely misreadings and ambiguity up front and adds probes so the wrong reading is caught early.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0622: FEATURE: Track open asks and who is asking (I009, value 3/5, effort S, risk low)
>   first version: Answer-debt list: fm second session already finds missed requests; first step is to surface it in fm next/status as 'unanswered asks' with a default and expiry. Small wiring.
>   what it is: Keeps answer debt, wrong-turn buttons and interpretation history visible.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0595, T-0601, T-0602, T-0621, T-0622 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0696. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0595: Split a message into its parts (I001, value 4/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_request.py -k Clauses`
- [x] T-0601: Turn steers into lasting rules (I003, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_request.py -k Steers`
- [x] T-0602: Learn from the user's reactions (I007, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_request.py -k Reactions`
- [x] T-0621: Defend against misreading (I002, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_request.py -k Misreading`
- [x] T-0622: Track open asks and who is asking (I009, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_request.py -k Asks`
## Non-goals
## Approach (options → choice → why)
Options: (a) a model pass over every user message; (b) small deterministic checks at intake, close and fm next, built on what exists (T-0439 steer proposals, T-0616 outcomes, the oracle child, fm second session's captures); (c) a per-prompt hook. Choice: (b): no per-turn cost. Clauses: fm clauses "<message>" splits a multi-part message and matches each clause to a recent or open task by shared words; unaccounted ones are kept until noted, and fm next names them. Steers: at close a steer worded as a standing rule (always, never, from now on, every time, going forward, by default) is listed as a rule candidate, and a standing 'no' becomes a veto proposal at once instead of after three repeats. Reactions: fm outcomes adds the fate 'corrected' when a correction is logged against a task after it closed. Misreadings: the oracle child also returns the worst plausible misreading with an intake probe, kept in the Oracle section. Asks: fm next lists the asks fm second session captured that are still unanswered, and fm tidy --apply defers (never drops) those older than 7 days.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0595: Split a message into its parts (I001, value 4/5, effort S, risk low)
2. [x] T-0601: Turn steers into lasting rules (I003, value 4/5, effort M, risk low)
3. [x] T-0602: Learn from the user's reactions (I007, value 4/5, effort M, risk low)
4. [x] T-0621: Defend against misreading (I002, value 3/5, effort S, risk low)
5. [x] T-0622: Track open asks and who is asking (I009, value 3/5, effort S, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: request understanding), ~/.claude/foreman/MASTER.md (fm clauses), ~/.claude/foreman/plugin/skills/intake/references/planning.md (every clause, misreadings)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_request.py` → ✗ exit 1 · Ran 5 tests in 1.4s (5 classes, 16 at a time; slowest: Reactions 1s, Steers 0s, Misreading 0s) / FAILED (5 classes) [ran] [tree 8d69d7614a2d] (2026-10-09T21:04:25Z)
- (step 1) `python3 plugin/tests/run.py -p test_request.py -k Clauses` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Clauses 0s) / OK [ran] [tree 47cc7fdfdd2e] (2026-10-09T21:05:34Z)
- (step 2) `python3 plugin/tests/run.py -p test_request.py -k Steers` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Steers 0s) / OK [ran] [tree 47cc7fdfdd2e] (2026-10-09T21:05:35Z)
- (step 3) `python3 plugin/tests/run.py -p test_request.py -k Reactions` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Reactions 1s) / OK [ran] [tree 47cc7fdfdd2e] (2026-10-09T21:05:37Z)
- (step 4) `python3 plugin/tests/run.py -p test_request.py -k Misreading` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Misreading 0s) / OK [ran] [tree 47cc7fdfdd2e] (2026-10-09T21:05:37Z)
- (step 5) `python3 plugin/tests/run.py -p test_request.py -k Asks` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Asks 0s) / OK [ran] [tree 47cc7fdfdd2e] (2026-10-09T21:05:38Z)
- (ac 1) `python3 plugin/tests/run.py -p test_request.py -k Clauses` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Clauses 0s) / OK [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- (ac 2) `python3 plugin/tests/run.py -p test_request.py -k Steers` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Steers 0s) / OK [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- (ac 3) `python3 plugin/tests/run.py -p test_request.py -k Reactions` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Reactions 1s) / OK [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- (ac 4) `python3 plugin/tests/run.py -p test_request.py -k Misreading` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Misreading 0s) / OK [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- (ac 5) `python3 plugin/tests/run.py -p test_request.py -k Asks` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Asks 0s) / OK [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1237 tests in 64.3s (407 classes, 16 at a time; slowest: Stop 38s, TaskLifecycle 25s, Parallel 22s) / FAILED (1 classes) [ran] [tree 3a2d71a12bde] (2026-10-09T21:06:53Z)
- (step 5) `python3 plugin/tests/run.py -p test_request.py -k Asks` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Asks 0s) / OK [ran] [tree f4db8634c6c5] (2026-10-09T21:09:02Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1237 tests in 64.5s (407 classes, 16 at a time; slowest: Stop 38s, TaskLifecycle 25s, Parallel 21s) / OK [ran] [tree f4db8634c6c5] (2026-10-09T21:10:06Z)
- (audit intent) `main-thread review of the diff against the five first versions; the full suite caught a conflict with T-0289, fixed` → the five first versions shipped as deterministic checks at intake, close and fm next; clause matching is lexical (2+ shared stems with a recent or open task) — a model reading would be the upgrade if clauses get missed [tree f4db8634c6c5] (2026-10-09T21:10:06Z)
- (audit adversary) `main-thread review of the diff against the five first versions; the full suite caught a conflict with T-0289, fixed` → fixed: fm next named the asks a child session found, inviting Claude to act on them, against T-0289 — now it only counts them as the user's to confirm and fm state marks them ✋; a standing steer only proposes a veto, adopted on the user's yes; expired asks are deferred, never dropped [tree f4db8634c6c5] (2026-10-09T21:10:06Z)
- (audit edge) `main-thread review of the diff against the five first versions; the full suite caught a conflict with T-0289, fixed` → a one-off steer stays out of the candidates (tested); a correction counts only after the task closed; clauses under three words are dropped so 'thanks!' isn't an ask [tree f4db8634c6c5] (2026-10-09T21:10:06Z)
## Log
- 2026-10-09T15:40:18Z created
- 2026-10-09T21:04:04Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_request.py -k Clauses`
- 2026-10-09T21:04:04Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_request.py -k Steers`
- 2026-10-09T21:04:04Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_request.py -k Reactions`
- 2026-10-09T21:04:05Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_request.py -k Misreading`
- 2026-10-09T21:04:05Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_request.py -k Asks`
- 2026-10-09T21:04:05Z focused
- 2026-10-09T21:10:07Z done
- 2026-10-09T21:10:07Z committed beca70c (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Lessons
- Surfacing something in fm next is an instruction to act on it; things only the user may settle belong in the user's view (fm state) and the end-of-run question, never in the model's next action
## Plan gaps
- failed first: step 1 T-0595: Split a message into its parts (I001, value 4/5, effort S, risk low)
## Files touched
- plugin/tests/test_request.py
- plugin/lib/fmcore.py
- plugin/lib/fmideas.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/planning.md
