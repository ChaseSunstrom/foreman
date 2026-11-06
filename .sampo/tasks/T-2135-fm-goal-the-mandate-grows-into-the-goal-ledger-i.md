---
id: T-2135
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T10:37:37Z
updated: 2026-10-31T01:50:03Z
base: c766ea50c80ab4beda850adc964aa66c56c023cc
base_tree: 6418fef4289b600c1531187649fa0a0595d24c7a
plan0_at: 2026-10-31T01:30:10Z
plan0_scope: []
verified: strong
---
# fm goal: the mandate grows into the goal ledger — items → tasks → done-when, coverage, one standing goal; fm mandate an alias (Mission 4 brief 1)
## Raw request
> fm goal: the mandate grows into the goal ledger — items → tasks → done-when, coverage, one standing goal; fm mandate an alias (Mission 4 brief 1)
## Interpretation
A goal is the project's one standing record of a sweeping request: its words, clauses, an end date, a USD bound (the mandate today), plus a contents list. Each item holds its source, a done-when and the tasks that build it. fm goal show is the ledger and its coverage.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal set/item/link/show: items link to tasks (fm goal link, fm task new --goal); show lists open tasks outside the goal, items with no task and items whose tasks closed while their done-when fails, exiting 1 when any; set refuses a second goal without --replace, which archives the first; a mandate with no items prints exactly as before — verify with `python3 plugin/tests/run.py test_goal test_mandate`
## Non-goals
## Approach (options → choice → why)
A (chosen, decided): grow fm mandate. B: a GOAL brief type with children via depends_on (schema change across queue/drive/archive). C: a light fm genesis per goal (too heavy). D: several goals per project (captured, revisit on two replacements of an unfinished goal). Revised after fm second plan (verdict revise): storage: the goal is the project meta's mandate record grown with items [{id, text, done_when, tasks}]; a mandate with no items reads as before, and fm mandate's output and exit codes stay byte-identical for it (tested). Drift, defined: (a) an open task linked to no item while a goal stands (work outside the goal), (b) an item with no linked task (a coverage gap), (c) an item whose tasks are all closed while its done-when check fails (claimed, not met); fm goal show lists each with counts and exits 1 when any exists. Links: manual (fm goal link ITEM TASK) and fm task new --goal ITEM stamp goal: on the brief; nothing is inferred. One standing goal: fm goal set refuses while one stands unless --replace, which archives the old goal with its items and links under goal_history marked replaced. text is required; until and usd stay optional as in fm mandate, and show prints 'no end date' / 'no budget' when absent. Order: record + set/item, then link and --goal stamping, then show, then ledger events. A brief with or without goal: is read the same by the queue, the drive and the archive (tested).
## Risks and rollback
## Execution prompt
## Steps
1. [x] goal record: items {n,text,source,done_when,tasks} on the mandate, fm goal set/item/link/show, test-first
2. [x] while a goal stands, new briefs are stamped goal:; coverage (items without tasks, goal tasks without items)
3. [x] ledger events goal_set/goal_item; docs
## Resume here
<!-- auto -->
- 2026-10-31T01:34:20Z step 1/3: goal record: items {n,text,source,done_when,tasks} on the mandate, fm goal set/item/link/show, test-first
- git: foreman/build; 5 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmmandate.py, plugin/tests/test_goal.py, plugin/tests/test_mandate.py
- touched since last checkpoint: plugin/tests/test_mandate.py, plugin/tests/test_goal.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2135.edit, plugin/lib/fmcli.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2135b.edit, plugin/lib/fmhooks.py, plugin/lib/fmmandate.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate` → exit 0 · Ran 11 tests in 2.6s (4 classes, 16 at a time; slowest: Goal 2s, GoalReview 1s, MandateAsBefore 0s) / OK [ran] [tree 9223fecf910f] (2026-10-31T01:42:11Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_mandate test_cli test_hooks test_scout` → exit 0 · Ran 391 tests in 38.0s (77 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree dca330ddd555] (2026-10-31T01:47:45Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate test_cli test_hooks test_scout` → exit 0 · Ran 391 tests in 38.0s (77 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree dca330ddd555] (2026-10-31T01:48:23Z)
- `cd plugin/tests && python3 -m unittest -q test_goal test_mandate` → ✗ exit 1 · Ran 10 tests in 1.498s / FAILED (failures=10) (start tree + this task's tests) [ran] [tree dca330ddd555] (2026-10-31T01:48:49Z)
- `cd plugin/tests && python3 -m unittest -q test_goal test_mandate` → exit 0 · Ran 10 tests in 4.088s / OK [ran] [tree dca330ddd555] (2026-10-31T01:48:49Z)
- (ac 1) `python3 plugin/tests/run.py test_goal test_mandate` → exit 0 · Ran 11 tests in 2.6s (4 classes, 16 at a time; slowest: Goal 2s, GoalReview 1s, MandateAsBefore 0s) / OK [ran] [tree dca330ddd555] (2026-10-31T01:49:02Z)
- (audit intent) `fm-reviewer five lenses on the uncommitted diff; fixed: a stored done-when now passes guard_stored at item time and before every run (a refused one is reported, never run; tested with a meta-injected pipe-to-shell check that leaves no sentinel), done-when plain'd and non-empty, fm goal set needs --until or an explicit --no-end, fm mandate on a goal is read-only (no checks, exit 0), checks bounded 300 s each and 900 s a show, fm mandate set/off archive a goal with items, gone tasks leave an item uncovered, a link moves a task, decimal item numbers only, the lock re-checks the goal; test_goal test_mandate test_cli test_hooks test_scout 391 green; red-to-green proven` → fm goal set/item/link/show and fm task new --goal; show lists outside work, uncovered items and claimed-but-unmet items, exit 1 on any; a second goal needs --replace, which archives; a plain mandate prints as before (now with the typed day) [tree dca330ddd555] (2026-10-31T01:49:02Z)
- (audit adversary) `fm-reviewer five lenses on the uncommitted diff; fixed: a stored done-when now passes guard_stored at item time and before every run (a refused one is reported, never run; tested with a meta-injected pipe-to-shell check that leaves no sentinel), done-when plain'd and non-empty, fm goal set needs --until or an explicit --no-end, fm mandate on a goal is read-only (no checks, exit 0), checks bounded 300 s each and 900 s a show, fm mandate set/off archive a goal with items, gone tasks leave an item uncovered, a link moves a task, decimal item numbers only, the lock re-checks the goal; test_goal test_mandate test_cli test_hooks test_scout 391 green; red-to-green proven` → a done-when is a stored command, so it gets the guard's checks at item time and before each run, like every verify fm runs (T-0901); an ended goal can't be renewed through goal set, item or link; fm mandate set/off are still unguarded, captured as T-2252 [tree dca330ddd555] (2026-10-31T01:49:02Z)
- (audit edge) `fm-reviewer five lenses on the uncommitted diff; fixed: a stored done-when now passes guard_stored at item time and before every run (a refused one is reported, never run; tested with a meta-injected pipe-to-shell check that leaves no sentinel), done-when plain'd and non-empty, fm goal set needs --until or an explicit --no-end, fm mandate on a goal is read-only (no checks, exit 0), checks bounded 300 s each and 900 s a show, fm mandate set/off archive a goal with items, gone tasks leave an item uncovered, a link moves a task, decimal item numbers only, the lock re-checks the goal; test_goal test_mandate test_cli test_hooks test_scout 391 green; red-to-green proven` → deleted tasks, a task linked twice, '²' as an item, an empty check, a concurrent fm mandate off, an until west of UTC printed a day late (fixed), a goal with no end said explicitly [tree dca330ddd555] (2026-10-31T01:49:02Z)
- (audit operator) `fm-reviewer five lenses on the uncommitted diff; fixed: a stored done-when now passes guard_stored at item time and before every run (a refused one is reported, never run; tested with a meta-injected pipe-to-shell check that leaves no sentinel), done-when plain'd and non-empty, fm goal set needs --until or an explicit --no-end, fm mandate on a goal is read-only (no checks, exit 0), checks bounded 300 s each and 900 s a show, fm mandate set/off archive a goal with items, gone tasks leave an item uncovered, a link moves a task, decimal item numbers only, the lock re-checks the goal; test_goal test_mandate test_cli test_hooks test_scout 391 green; red-to-green proven` → checks run only from fm goal show, bounded 300 s each and 900 s in all; past the budget an item says check not run; fm mandate stays cheap and read-only [tree dca330ddd555] (2026-10-31T01:49:02Z)
- (audit maintainer) `fm-reviewer five lenses on the uncommitted diff; fixed: a stored done-when now passes guard_stored at item time and before every run (a refused one is reported, never run; tested with a meta-injected pipe-to-shell check that leaves no sentinel), done-when plain'd and non-empty, fm goal set needs --until or an explicit --no-end, fm mandate on a goal is read-only (no checks, exit 0), checks bounded 300 s each and 900 s a show, fm mandate set/off archive a goal with items, gone tasks leave an item uncovered, a link moves a task, decimal item numbers only, the lock re-checks the goal; test_goal test_mandate test_cli test_hooks test_scout 391 green; red-to-green proven` → the goal lives on the mandate record (no new store), archiving in one _archive used by put and clear; show and cmd_mandate share one renderer [tree dca330ddd555] (2026-10-31T01:49:02Z)
## Log
- 2026-10-30T10:37:37Z created
- 2026-10-30T19:00:53Z set approved=True
- 2026-10-30T19:00:53Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-31T00:15:08Z criterion 1 text: fm goal set/item/link/show keep items linked to tasks, show coverage gaps and drift, and fm mandate still works → fm goal set/item/link/show: items link to tasks (fm goal link, fm task new --goal); show lists open tasks outside the goal, items with no task and items whose tasks closed while their done-when fails, exiting 1 when any; set refuses a second goal without --replace, which archives the first; a mandate with no items prints exactly as before
- 2026-10-31T00:15:08Z fm second plan: revise; plan revised (storage in the mandate meta with a byte-identical old path, drift defined as three lists, manual and --goal links only, --replace archives, optional until/usd, step order fixed, brief tolerance tested)
- 2026-10-31T01:30:10Z focused
- 2026-10-31T01:34:30Z paused: focus moved to T-2154
- 2026-10-31T01:40:49Z focused
- 2026-10-31T01:48:24Z scope: plugin/lib/fmmandate.py, plugin/lib/fmcli.py (task new --goal, the goal parser), plugin/lib/fmhooks.py (one date), plugin/tests/test_goal.py, plugin/tests/test_mandate.py, MASTER.md, CHANGELOG.md
- 2026-10-31T01:48:24Z steer: approved per the user's 'I approve all changes'; plan revised after fm second plan
- 2026-10-31T01:50:02Z done
- 2026-10-31T01:50:03Z committed 3e8600d5 (7 files)
## Follow-ups captured
## Build vs reuse
Reuses: fm mandate (meta's mandate record, session-start display, T-2186's renew-is-the-user's-call rule) grown in place rather than a new store; briefs and depends_on for items to tasks; fm genesis coverage's grid pattern for goal coverage; fm next for the standing goal's next item. New: the goal ledger's items and done-when, fm goal as the verb with fm mandate kept as an alias.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The acceptance criterion only proves the commands run and tests pass, not that the request holds. "Keep items linked to tasks, show coverage gaps and drift" is untestable as written, because "drift" is never defined anywhere in the plan (drift from what: the goal text, the end date, the USD b…
- HIGH: There is no migration or backward-compat plan for existing mandates. The goal "grows" the mandate, but the plan doesn't say where the record is stored, what happens to an existing mandate file with no items, or whether `fm mandate` output and exit codes stay byte-identical for current callers…
- MEDIUM: Step 1 puts `link` and `show` in the same step as the record and `set`/`item`, while the stamping that makes links automatic (`goal:` on new briefs) comes in step 2. Until then, links are manual only, and `show` coverage has nothing to compute against. Also, ledger events (step 3) come last…
- MEDIUM: Edge semantics are unspecified for "one standing goal." What does `fm goal set` do when a goal already stands: replace, refuse, or archive the old one? Option D says "revisit on two replacements of an unfinished goal," which implies replacement happens, but nothing says the old items and ta…
- MEDIUM: Stamping new briefs with `goal:` (step 2) touches the brief creation path, which is shared by queue/drive/archive, the same surface Option B was rejected for. The plan doesn't check that adding a front-matter field is tolerated by those consumers. — Add a test that briefs with and without `…
- LOW: The USD bound and end date are carried over from the mandate, but the plan doesn't say whether `goal set` requires them, or accepts a goal without a bound (the mandate presumably needs one). — State which fields are optional and what `show` prints when they are absent.
Verdict: revise — the direction is sound and the cheap approach is reasonable, but "drift" is undefined, the existing-mandate migration is unplanned, and the acceptance test doesn't demonstrate the request, so tigh…
## Dissent
- [ ] HIGH: The acceptance criterion only proves the commands run and tests pass, not that the request holds. "Keep items linked to tasks, show coverage gaps and drift" is untestable as written, because "drift" is never defined anywhere in the plan (drift from what: the goal text, the end date, the USD b…
- [ ] HIGH: There is no migration or backward-compat plan for existing mandates. The goal "grows" the mandate, but the plan doesn't say where the record is stored, what happens to an existing mandate file with no items, or whether `fm mandate` output and exit codes stay byte-identical for current callers…
- [ ] MEDIUM: Step 1 puts `link` and `show` in the same step as the record and `set`/`item`, while the stamping that makes links automatic (`goal:` on new briefs) comes in step 2. Until then, links are manual only, and `show` coverage has nothing to compute against. Also, ledger events (step 3) come last…
- [ ] MEDIUM: Edge semantics are unspecified for "one standing goal." What does `fm goal set` do when a goal already stands: replace, refuse, or archive the old one? Option D says "revisit on two replacements of an unfinished goal," which implies replacement happens, but nothing says the old items and ta…
- [ ] MEDIUM: Stamping new briefs with `goal:` (step 2) touches the brief creation path, which is shared by queue/drive/archive, the same surface Option B was rejected for. The plan doesn't check that adding a front-matter field is tolerated by those consumers. — Add a test that briefs with and without `…
- [ ] LOW: The USD bound and end date are carried over from the mandate, but the plan doesn't say whether `goal set` requires them, or accepts a goal without a bound (the mandate presumably needs one). — State which fields are optional and what `show` prints when they are absent.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
- T-1400 [FEATURE M, done, 1 steps] A standing mandate: a sweeping request becomes one record (its text, its clauses from fm c — lesson: parse_ts returns a datetime, not e…
- research T-2146-review: Changes needed. These are two small, cheap fixes, not a redesign. [stale: plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_hooks.…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
## Lessons
- A new runner of stored commands must route through the guard's stored-command check; grep the existing runners (guard_stored) before adding one
## Files touched
- plugin/tests/test_goal.py
- plugin/tests/test_mandate.py
- plugin/lib/fmcli.py
- plugin/lib/fmmandate.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmgenesis.py
- plugin/tests/genesis_page.js
- plugin/tests/test_genesis.py
- plugin/tests/test_site_build.py
- site/genesis/genesis.css
- site/genesis/genesis.js
- site/genesis/index.html
