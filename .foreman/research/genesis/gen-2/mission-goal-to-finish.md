# Mission 7 — goal to finish (gen 2, #4)

Task: T-2556, T-2557, T-2558 (briefs 1-3 in order; T-2558 deferred with its revival condition).

Parent: gen-2/seed.md row 7 → gen-0.md #4 ("Goal to finish. Turn a vague goal into a complete plan: what a finished,
best-in-class version contains, decomposed and ordered. It carries the plan over days, across crashes and
compactions, and knows when it's actually done rather than merely stopped…"). gen-0's goal, MUSTs and NEVERs are
quoted in the seed and apply here unchanged.

## Capability
Knowing a long goal is done rather than merely stopped. The machinery for short tasks is built: done-when checks
that must fail on the start tree (T-2416), fm task finish refusing on a red gate (T-2526), goal items done only when
no linked task is open (fmmandate.item_state), resume across compactions.
What fails, on the long-horizon tier (fm exam long grade, replays of six goals from Foreman's own history each):
on l001 the foreman arm reached 0 of 6 true dones and said done on all 6 (5 of 20 hidden checks passing). On l002
foreman scored 0 of 6 with 6 false dones (4 of 20 checks), and plain Claude 1 of 6 with 5 false dones (4 of 20),
both for about $13. The sessions' own done-when checks pass while the goal's hidden checks fail, so the plan missed
parts of the goal, and Foreman does no better than plain. A smaller gap, also with failures on record: user-only
needs are found mid-run (3 grant_queued events, T-2542's system ask among them).

## Grounding
- Brief 1: fm exam long grade l001/l002 --agent foreman (plugin/lib/fmlong.py) shows false_done 6 of 6 with 0-2
  hidden checks of up to 5 passing per goal; nothing yet records which checks failed against what the session planned.
- Brief 2: fm goal plan (plugin/lib/fmmandate.py) turns a goal into items and done-when checks but never re-reads the
  goal's request against what was delivered before a done claim; fm clauses accounts for a request's clauses only.
- Brief 3: fm goal plan names no guard categories; the ledger's 3 grant_queued events were all found mid-task.

## Gaps this Mission targets (coverage: #4, 58 empty cells; the I cells below are planned, open until the exam closes them)
- Why long goals false-done: verify × headless/server, learn × headless/server (a per-goal diagnosis from the runs on
  disk: each failed hidden check against the session's own plan and done-when).
- A done claim checked against the whole goal: verify × CLI, plan × Claude Code (before a goal session claims done,
  every requirement the goal states is matched to delivered work or named as missing).
- User-only needs at plan time: plan × CLI (carried, see brief 3).

## Approaches
1. Diagnose first, then build: brief 1 reads l001 and l002's work trees, keys and fault logs at zero tokens and
   classes each failed check (never planned, planned but not built, built but broken, check out of the goal's
   reach). Brief 2 builds against the largest class, likely a done-claim audit of the goal's requirements. Fails if:
   the classes say the hidden checks ask for what the goal never stated. The answer: Foreman never rewrites
   its own exam's keys. That finding goes into the final report for the user, and any re-keying is done by the
   tool-less child author (--author child), which never sees the Missions. Brief 2 then targets the next class.
2. Raise the bar with more verification turns per session. Fails if: the plan, not the checking, missed the
   requirement; more turns verify the wrong list harder.
3. Ask a model to judge done. Fails if: models advise and proof decides; a judged done is still unproven.
4. Use what exists: fm clauses already accounts for a request's clauses, fm goal verdict already blocks a done with
   an open item, and fmlong keeps every run's tree. Brief 2 extends the clause accounting to goal sessions.
5. Do less: report the false-done count as the headline number and change nothing. Fails if: 6 of 6 stays 6 of 6.

Choice: 1 on 4 (70%). The 30% doubt is that the diagnosis points at the exam's keys rather than at Foreman.

## Exam
#4's kinds are goal and resume, and the long-horizon tier decides. Brief 1 is graded by its own record: every failed
hidden check on l001 and l002 placed in one class, with the evidence path. Brief 2 is graded at the end-of-run exam
(rule 6: session arms wait for --final): foreman's false dones on the long tier must fall below plain's on the same
goals. Zero-token arms run each generation.

## Long-horizon goal (end of run)
On the end-of-run long tier, foreman's false-done count is below plain's on the same goals, and below 6 of 6.

## Lean
Brief 1 adds no runtime code (a research record). Brief 2 runs once per goal done claim, never in a hook. Brief 3 is
carried.

## Tier share
Briefs 1 and 2 are tier 4: Foreman lacks any check that a long goal's done claim covers the goal, and the exam shows
it at 6 of 6. Brief 3 is tier 3, carried. Two of three are tier 3-4 and built this generation.

## Done when
Brief 1's diagnosis is filed as research with every failed check classed. Brief 2 is built against the largest
class, with a red-to-green test, and waits for the end-of-run long tier for its verdict. Brief 3 is carried with its
revival condition.

## Briefs (fm intake)
```
RESEARCH: why long goals false-done: read fm exam long's l001 and l002 runs at zero tokens and class every failed hidden check (never planned, planned but not built, built but broken, out of the goal's reach) against each session's own plan and done-when; file it as research long-false-done
FEATURE: a goal's done claim is checked against the whole goal: before a goal session claims done, each requirement the goal states is matched to delivered work or named missing, built against the largest class brief 1 finds
FEATURE: user-only needs at plan time: fm goal plan classifies each item's done-when and step commands with fmguard (classify only) and lists the guard categories that need the user; revives at 5 mid-run grant_queued events within 30 days
```
