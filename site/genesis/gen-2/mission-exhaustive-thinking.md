# Mission 5 — exhaustive thinking (gen 2, #2)

Task: briefs 1-2 in order (ids assigned at intake).

Parent: gen-2/seed.md row 5 → gen-0.md #2 ("Exhaustive thinking. Before acting on anything non-trivial: list the
readings of the request, every approach (including 'use what exists' and 'do less')…"). gen-0's goal, MUSTs and
NEVERs are quoted in the seed and apply here unchanged.

## Capability
Thinking that starts from what already exists. Grounded before filing, most of #2 is built: the plan gate asks M and L
tasks for two readings, three or more options each with how it fails, a use-what-exists and a do-less option, and a
stated Choice percent (T-2335). The cold rival reads the request without the plan (fm second rival), races and the door
gate act on the result, blast radius answers "unknown" when there's no co-change history (T-2277), and confidences are
scored (Mission 2). Brainstorm ideas grounded and not built now: a blind-graph answer for blast radius is an exact
duplicate (built, T-2277). Two are queued as tasks deferred to 2026-12-01, each with a revival condition.
Model-substitution checks on deliberation children (T-2544) revive at the first child answer recorded on a model
other than the one asked; none is on record. Voiding races scored on a flaky verify (T-2545) revives once races run
here (no race has been picked yet) and one is scored on a flaky check.
What it lacks, with the failures on record: the use-what-exists question is asked at planning, after a task already
exists, and nothing at a task's birth checks what Foreman already holds. 47 of the 381 dropped tasks' drop notes say
the work was already built or already existed. That's about one drop in eight, each a capture, a grounding pass and a
drop. The existing nudge (fmrecall.covered, T-0256) compares a request only with fm's help text. The same gap showed
in the tower today: Mission 3 filed five briefs, and three were built, or had no failure behind them, which planning
found only after filing (T-2533, T-2534, T-2535).

## Gaps this Mission targets (coverage: #2, 58 empty cells; the I cells below are planned, open until the exam closes them)
- Planned, existing work checked at a request's birth: find × CLI, understand × CLI, plan × Claude Code (once built,
  fm capture and fm task new name the closest MASTER.md clauses and their task ids when a request mostly restates
  one; MCP is read-only here, so it has no capture path to check).
- Grounded Missions: plan × headless/server, understand × Claude Code (fm genesis put of a Mission refuses an intake
  block with no grounding line per brief: the code that lacks it, and the record that its failure happened).
- Not in this Mission: model checks on children (T-2544) and race scoring (T-2545), both deferred with revival conditions; the plan's fork-map view and a Thinking workspace on the
  site. They stay idea cells.

## Approaches
1. Extend the nudge that exists. fmrecall.covered also reads MASTER.md's module entries, split at their semicolons
   into clauses, each carrying its task id. fm capture and fm task new print the best two clauses that the request
   mostly restates. Fails if: long clauses match everything. The answer: the same thresholds as the help match (three
   or more shared words, most of the clause's), and a backtest on the 381 dropped and the done tasks decides the
   thresholds before it prints anything.
2. Refuse a capture that matches an existing clause. Fails if: a near match is a real extension (a new flag on an old
   verb), and a refusal blocks the work. A nudge informs and never refuses.
3. Ask a model whether the request is built. Fails if: a model's opinion becomes the gate. Models advise and proof
   decides (the model layer's rule), and the word match is free and local.
4. Use what exists: fmrecall.covered, its thresholds and its print sites are there already. Approach 1 adds a second
   corpus, MASTER.md, which every task's docs step already keeps current.
5. Do less: a rule line asking the session to grep MASTER.md first. Fails if: rules don't run, and the 47 drops
   happened with the rules in place.

Choice: 1 on 4 (75%). Brief 1's backtest decides whether the nudge ships: it must flag at least a third of the 47
built drops while flagging under 1 in 10 of the done tasks that were new work. The 25% doubt is that word overlap is
too blunt for MASTER's long clauses. If the backtest fails, the brief closes on that result, and nothing prints.

## Exam
#2's exam kinds are vague and ambiguous (a request with more than one reading), and exists (the request asks for what
@clamp@ already does, T-2216). Brief 1 is graded first by its backtest, against outcomes Foreman didn't choose: which
tasks the user's work later dropped as already built, and which were done as new work. It is graded second by the
exists kind's held-out scenarios at the end-of-run exam. Brief 2 is graded by the next Mission filed: its briefs carry
grounding lines, and none is dropped at planning as built. Zero-token arms run each generation.

## Long-horizon goal (end of run)
Across the long-horizon goals, the share of tasks dropped as already built falls below the 1-in-8 measured now, and
no gen-3 Mission brief is dropped at planning for being built.

## Lean
No new verb. fmrecall.covered gains a second corpus, read at capture time only (no hook). The nudge prints two lines
at most, and only on a match. fm genesis put gains one check for Mission files. Hook p95, rules size and injected
context don't grow.

## Tier share
Brief 1 is tier 3, a capability Foreman lacks: checking a request against what it already holds at the request's
birth, not at planning. Brief 2 is tier 2. One of two, 50%.

## Done when
A capture or task whose request mostly restates a MASTER.md clause prints that clause and its task id, with
thresholds the backtest set (a third or more of the built drops flagged, under 1 in 10 of new work), or the brief
closes on the backtest's failure with nothing printed. fm genesis put refuses a Mission whose briefs have no
grounding lines.

## Briefs (fm intake)
```
FEATURE: already built, at birth: fmrecall.covered also matches the request against MASTER.md's module clauses (split at semicolons, each with its task id), and fm capture and fm task new print the best two; thresholds set by a backtest on the dropped-as-built and done tasks (flag a third or more of the built drops, under 1 in 10 of new work), else nothing prints
FEATURE: grounded Missions: fm genesis put refuses a Mission file whose intake block has a brief with no grounding line (a '## Grounding' section naming, per brief, the code that lacks it and the record that its failure happened)
```
