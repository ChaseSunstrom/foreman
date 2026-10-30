# Mission — Goal to finish (gen 1, #4)

Task: T-2135…T-2141 (briefs 1–7 in order). T-2135 is L: today's spent risk budget is Foreman's own guard, which
gen-0 forbids lowering, and it holds L self-approval until it resets on 2026-10-31; no question goes to the user,
and then the plan takes the normal L path under full autonomy (a self-critique, then `fm decide`). Nothing is
granted around the guard while it's spent; the run waits it out, as it would a usage limit.

Self-contained for a fresh `fm run` in ~/.claude/foreman. Parent: gen-1/seed.md → gen-0.md §2 #4, §3.
Ideas: 308 from `fm ideas --rounds 4 --falsify --crossbreed --seen` (mission pack research/mission-20261030-053122.md;
`--deepen` didn't run: the spent risk budget drops optional rounds, a guard Foreman never lowers itself; decisions.md
2026-10-30 "Mission 4 brainstorm ran without --deepen", revisit after 2026-10-31: the deepen rounds rerun and merge
here), lenses below; placed by tier
after merging duplicates.

## Capability (gen-0 §2 #4)
Turn a vague goal into a complete plan: what a finished, best-in-class version contains, decomposed and ordered. It
carries the plan over days, across crashes and compactions, and knows when it's actually done rather than merely
stopped.

## What the last Missions taught
- Precision over volume (Mission 2, 3): both session arms found every planted defect and closed no scenario. For #4
  the same trap is "done": a session that says done while a contents item is missing is the false alarm here.
- A live arm finds what fixtures don't (a table-less seed broke a live run that unit tests passed).
- One reviewer pass per task catches what its own tests didn't.
- Every surface, or it isn't done: CLI, Claude Code hooks and pane, fm code, MCP, other agents, Desktop, site.

## Lenses (pack: required + invented + fitted)
- Required: **inversion** (how finishing fails: stops early, calls it done when it merely stopped, loses the plan to a
  compaction or crash, plans an incomplete version, drifts off the goal, gold-plates forever); **sci-fi** (the 2030
  harness that takes one line and works for weeks to a finished result, worked back to a ledger, a verdict and a hook
  today); **self-modification** (a planner that learns from which plans held: every item added after "done" is a miss
  the next contents list prevents, measured per goal, reversible).
- Invented: **the reopened ticket** (what a user finds missing a week after done); **relay race** (a fresh session with
  zero memory resumes mid-goal exactly; the plan on disk is the only memory); **done-vs-stopped auditor** (an adversary
  that tries to prove the work merely stopped: usage limit, drive cap, no-progress stop, crash, the model saying done).
- Fitted: user value, reliability, simplicity, bold bets, blind spots.

## Gaps this Mission targets (gap map #4; planned briefs, open until the exam shows them closed)
| Gap | Tier | Brief |
|---|---|---|
| A goal ledger: contents → tasks → done-when → coverage, one record a goal lives in; epics | 4 | 1 |
| Grounded contents lists: from the user's words, the repo's surfaces and the finish standard | 3 | 2 |
| Done-vs-stopped verdict with the stop's cause | 4 | 3 |
| Clauses wired to Stop: an unmet MUST or DONE-WHEN clause blocks "done" | 3 | 4 |
| The goal carried across days, crashes and compactions | 3 | 5 |
| No held-out, child-authored exam for #4 | 3 | 6 |
| Surfaces: fm code, MCP, other agents, Desktop, site, pane, docs | 3 | 7 |

## Approaches
A. **Chosen — grow `fm mandate` into the goal ledger** (decided). The mandate is already the standing record of a
   sweeping request (text, clauses, until, a USD bound) that scout and the night run read. It gains contents items,
   each linked to its tasks and done-when, and a verdict. One standing goal per project; epics are contents items with
   several tasks. `fm goal` is the verb; `fm mandate` stays an alias.
B. A GOAL brief type whose children hang off `depends_on`. Not now: a schema change across queue, drive, archive and
   site for what one record holds.
C. A light `fm genesis` per goal (gen-0 → missions → briefs). Too heavy for an everyday goal; #13 keeps it for goals
   that rewrite Foreman itself. The ledger is what genesis's tower would read if it grows into goals.
D. Several standing goals per project. Captured: revisit when a user replaces an open goal with another while the
   first is unfinished, twice.

## Design
1. **Goal ledger — `fm goal`** (tier 4, L). `fm goal set "<goal>" [--until] [--usd]` (the mandate record grows
   `items`: `{n, text, source, done_when, tasks}`); `fm goal show` the ledger: each item → its tasks → their status and
   done-when; coverage: items with no task, open tasks captured under the goal with no item (drift); `fm goal link N
   ID`, `fm goal item "<text>" [--done-when "<check> :: <cmd>"]`. While a goal stands, `fm capture`/`fm task new`
   stamp `goal:` on the brief, and `fm goal link` places it. Ledger events `goal_set`, `goal_item`, `goal_verdict`.
2. **Grounded contents list — `fm goal plan`** (tier 3, M). Items from three sources, each tagged: the user's words
   (fmrecall.clauses, one item per clause, source `user`); the finish standard for what the repo actually ships
   (fmmission.surfaces: tests, exam scenarios, MASTER/README/CHANGELOG, a site page if user-facing, a pane line if it
   has state, each surface it belongs on; source `standard`); and a tool-less child's best-in-class list from the
   mission pack (source `model`), kept only when it names a file, symbol or surface the repo has or a user clause
   implies; the rest are shown as proposals, never items. Naming a real file is only the grounding floor, not proof
   the item matters: whether the list was right is scored by misses and by the goal exam kind (brief 6). Misses learn:
   an item added after the goal's first done claim, or a revert, re-fix or correction within 30 days of a task's close
   (fm outcomes' window), is a miss recorded by surface; `fm goal plan` adds the
   project's top misses as checklist lines and says how many past goals missed each.
3. **Done-vs-stopped verdict — `fm goal verdict`** (tier 4, M). Deterministic. **Finished** only when every item has a
   task and every task is done (a dropped one needs its logged reason), every done-when command passes on a fresh
   run now, no clause of the goal is unaccounted, and the gates are green on HEAD (fm check's same-tree reuse).
   Otherwise **stopped**, with the cause read from the ledger and the session events: usage limit, drive cap
   (DRIVE_MAX), no-progress stop, contract bound spent, waiting on the user (an open `fm ask`), paused, crash (a
   session start with no Stop after the last edit), or the model saying done with items open. Prints what's left in
   order. The verdict is Foreman's own check, so it never counts as outside proof: the goal and resume exam kinds
   (brief 6) score its false-done rate against a hidden key it never sees, and fm outcomes scores it after 30 days.
4. **Stop wired to the goal and the clauses** (tier 3, M). In `stop()`: a done claim (claims_done) while the last
   request has unaccounted clauses (fm clauses' `open`) blocks once with them; while a goal stands and its verdict is
   stopped, a done claim blocks once with the items left. Both count toward DRIVE_MAX and the no-progress stop, so
   they never trap a session. The drive, with an empty queue and an open goal item with no task, says "plan item N"
   instead of ending (full autonomy) or names it (standard).
5. **Goal across days** (tier 3, M). SessionStart and the PreCompact checkpoint carry one line: the goal, items
   done/total, the next item and its task; `fm resume` prints it; `fm run` takes the next item's task when the queue
   is empty. A goal set by a past session is re-injected every session until its verdict is finished or it is cleared.
6. **#4 exam kinds** (tier 3, M). `goal`: a tool-less child, shown only the scenario's generated module and the
   scenario format (never Foreman's code or the Missions), writes a vague goal for that module and a hidden contents
   key (4–6 items: each a test body or a README pattern), the arm gets only the goal; graded on key items met, 0
   regressions, and whether the arm's final claim matches the truth (said done with a key item unmet = a false done).
   `resume`: the same goal with half its items done and the plan on disk, the first session killed; a fresh session
   gets "continue"; graded on the remaining items met and no item redone. Child-authored, 9 per kind (3 held out),
   six languages.
7. **Surfaces** (tier 3, M). fm code (the goal line in its prompt and the same stop check), the MCP tool list (`goal`,
   read-only: ledger and verdict), the AGENTS.md block for other agents, Desktop through MCP, the site page (Goal to
   finish: items, verdicts over time, the exam line), the pane band (a goal progress line), MASTER.md, README,
   CHANGELOG.

## Exam (#4; ≥ 9 scenarios per kind, ≥ 3 held out)
| Kind | Given | Graded on |
|---|---|---|
| G-goal | a vague goal for the module, a hidden contents key (4–6 items) | key items met; 0 regressions; no false done |
| G-resume | the goal half done, the plan on disk, the first session killed; "continue" | remaining items met; none redone |
Arms: foreman (fm goal + Stop), plain ("" plugin), on the held-out third, with cost. The oracle meets every key item;
empty meets none and must never be graded done.
These kinds are the smoke tier (gen-1/seed.md rule 6): small single-defect scenarios never decide #4 on their own. The deciding end-of-run score is the long-horizon tier, on the production model: a goal replayed from Foreman's own history (the repo rolled back to the parent of a past multi-task change, that change's request as the goal, its shipped tests as the hidden checks), with a killed session and a forced compaction planted mid-run. Scored per finished goal on true-done rate, false-done claims, regressions and later reverts, interventions needed and cost per finished goal.

## Exam of the exam
1. Every key item's test passes on the oracle's render and fails on the base, in all six languages.
2. A child's key item that the base already meets is dropped and logged as an exam defect.
3. Held-out ids never appear in a train run or in tuning the contents checklist.

## Spikes (tier 4, local, throwaway)
Relay race: kill a session at five random points of a goal, a fresh one resumes from disk alone; count redone and lost
items. Reopened-ticket miner: in git history, commits within 30 days of a task's close touching its files are misses;
does `fm goal plan`'s list predict them? Done-vs-stopped adversary: craft states that make the verdict say finished
wrongly (a done-when that passes vacuously, a dropped task with no reason).

## Inbox (tier 1–2, captured)
- T-2142 goal notices only on state transitions (tier 2)
- T-2143 a byte-stable goal card so the SessionStart prefix stays cached (tier 1)
- T-2144 the goal's remaining distance as one number on the statusline and terminal title (tier 2)
- T-2145 a time-to-finish estimate from the items' history (tier 2)

## Rejected
Nothing for ambition. Only the outward halves, which need a grant the Mission can't take:
- "Publish mortality tables of how goals end": publishing leaves the machine. The local table lives in brief 3's verdict history.
- "Nudge a wrist or phone on a typed wait": outward without a grant. `fm notify` is the user's opt-in path, and T-2142 feeds it.
- "Take steers from a synced drop folder": a sync channel is outward. `fm sync` and `fm serve` already cover it under their grants.

## Tier share
Briefs: 7 (tier 4: 1 and 3; tier 3: 2, 4, 5, 6, 7), so 100% of the Mission's work is tier 3–4, plus 3 tier-4 spikes. The 4 inbox items (tier 1–2) are captured, not Mission work.

## Done when
`fm goal set/plan/show/verdict` work and are tested; a done claim with unaccounted clauses or an unfinished goal is
blocked once at Stop and never traps the session; the goal line survives a new session, a compaction and a crash; the
#4 exam runs the foreman and plain arms on its held-out third; fm code, MCP, the AGENTS.md block, the site page, the
pane line, MASTER.md, README and CHANGELOG show it.

```
FEATURE: fm goal — the mandate grows into the goal ledger: items → tasks → done-when, coverage, one standing goal
FEATURE: fm goal plan — a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn
FEATURE: fm goal verdict — finished vs stopped, with the stop's cause, deterministic
FEATURE: Stop wiring — unaccounted clauses and an unfinished goal block a done claim once
FEATURE: goal across days — SessionStart, PreCompact, fm resume and fm run carry the goal line
FEATURE: #4 exam — G-goal and G-resume, child-authored, foreman vs plain
FEATURE: goal surfaces — fm code, MCP, AGENTS.md, site page, pane line, docs
DONE-WHEN: #4's held-out exam passes at the end-of-run exam (the production-model foreman-vs-plain and long-horizon runs
decide, gen-1/seed.md rule 6); until then the free arms and the Haiku smoke run show no regression, and no arm is graded done while
a key item is unmet
```
