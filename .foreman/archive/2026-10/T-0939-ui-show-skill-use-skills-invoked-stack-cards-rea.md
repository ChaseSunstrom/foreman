---
id: T-0939
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:08:36Z
updated: 2026-10-15T20:50:50Z
base: a113cda15b86dca03a924b647edb9605977e1b02
base_tree: 3577cf87b9b875c71351efff41deb6e31cd73152
verified: ok
---
# Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards
## Raw request
> UI: show skill use (skills invoked, stack cards read, plugin skills) and keep super-improving the pane with more features
## Interpretation
The user wants to see skill use in the pane. gather() in fmwatch.py already tails events.jsonl (kind tool, tool Skill, target 'plugin:skill', ts) and the project ledger, which now has 'lib' events from fm lib show (data.cards). The map holds the repo's suggested cards (map.json 'lib'). Done means fm ui --json carries a skills block, {recent: [{name, kind: skill|card, at}], counts: {name: n} over 7 days, suggested: [names], unread: [suggested names not read this week]}, and the mod draws a Skills card: recent skills and cards as chips with their age, a top-used sparkline, and unread suggestions dimmed as 'fm lib show NAME'. A live Skill call also flashes in Now.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ui --json carries skills: recent (at most 8, newest first: this project's Skill tool calls by plugin:skill name and fm lib card reads, last 7 days), counts (per name, 7 days), suggested (map.json's lib list, [] when there's no map or no lib key) and unread (suggested cards not read in 7 days); a missing map, malformed JSONL lines or events without ts give an empty or partial block, never an error — verify with `python3 plugin/tests/run.py -k UiSkills`
- [x] The pane's Skills card shows the recent ones as chips with their age, the top counts, and unread suggestions dimmed as 'fm lib show NAME'; it is hidden when the block is empty; folded, its head still says 'N unread' — verify with `claude plugin test mods/foreman-ui`
## Non-goals
No live flash in Now for a Skill call (no criterion proves it; the recent chips cover it). No new fm verb.
## Approach (options → choice → why)
Options: (A) build the block in fmwatch.view from what gather() already reads, plus map.json, and add one Skills card in register.tsx that reuses chip, head and spark (chosen: no new state, one read path); (B) a separate fm skills verb the mod polls (a second process per refresh); (C) the mod parses the transcript for Skill calls itself (misses fm lib reads and other sessions). Placement: under Plan, folded by default the way the quieter cards are (T-0914), so it adds no height to a busy pane. The view key also goes in types/index.d.ts and test_ui's shape check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] View: skills block in fmwatch.view from events and ledger, with a test
2. [x] Mod: Skills card and live chip on each Skill call, with tests
3. [x] README pane description and a fresh shot
## Resume here
## Docs impact
README.md pane description names the Skills card (fm lib show NAME)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k UiSkills` → ✗ exit 1 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: UiSkills 0s) / FAILED (1 classes) [ran] [tree 1a27b4326bc2] (2026-10-15T20:41:04Z)
- (step 1) `python3 plugin/tests/run.py -k UiSkills` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: UiSkills 0s) / OK [ran] [tree bfe120d4c1f0] (2026-10-15T20:41:57Z)
- (step 2) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 85 tests across 1 file. [10.82s] [ran] [tree 4d50ad2987bb] (2026-10-15T20:43:43Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 85 tests across 1 file. [8.90s] [ran] [tree 8529199df56a] (2026-10-15T20:44:21Z)
- (step 3) `grep -c 'fm lib show NAME' README.md` → exit 0 · 1 [ran] [tree f2208bce85c5] (2026-10-15T20:44:34Z)
- (step 1) `python3 plugin/tests/run.py -k UiSkills` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: UiSkills 1s) / OK [ran] [tree 17378abaee73] (2026-10-15T20:46:19Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 85 tests across 1 file. [8.72s] [ran] [tree 17378abaee73] (2026-10-15T20:46:36Z)
- (ac 1) `python3 plugin/tests/run.py -k UiSkills` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: UiSkills 1s) / OK [ran] [tree 7d0c2198b414] (2026-10-15T20:49:50Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 86 tests across 1 file. [8.48s] [ran] [tree 7d0c2198b414] (2026-10-15T20:50:01Z)
- (step 3) `shot.py snap of a demo project after fm lib show python bash (scratchpad ui-skills.png)` → Skills card under Plan: 'python 1m ago · bash 1m ago', 'top: python ×1 · bash ×1', fold control in its head [tree 7d0c2198b414] (2026-10-15T20:50:32Z)
- (ac 1) `python3 plugin/tests/run.py -k UiSkills` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: UiSkills 1s) / OK [ran] [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 86 tests across 1 file. [8.53s] [ran] [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
- (audit intent) `main-thread review of the branch (fmwatch._skills, the Skills card, types, tests) plus a live shot; fixed a bold→weight sed slip at register.tsx:905 found while merging` → ok: recent skills and cards with age, top counts, unread suggestions dimmed as fm lib show NAME, hidden when empty, folded head keeps the unread count [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
- (audit edge) `main-thread review of the branch (fmwatch._skills, the Skills card, types, tests) plus a live shot; fixed a bold→weight sed slip at register.tsx:905 found while merging` → ok with a ceiling: a whole-file scan of events.jsonl filtered by substring (9 ms at 2.8 MB); rotated logs aren't read, so a week spanning a rotation is partial [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
- (audit operator) `main-thread review of the branch (fmwatch._skills, the Skills card, types, tests) plus a live shot; fixed a bold→weight sed slip at register.tsx:905 found while merging` → ok: README pane line names the Skills card [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
- (audit maintainer) `main-thread review of the branch (fmwatch._skills, the Skills card, types, tests) plus a live shot; fixed a bold→weight sed slip at register.tsx:905 found while merging` → ok: _grep_jsonl and _skills are small and tested with malformed, old, foreign and missing inputs [tree 7d0c2198b414] (2026-10-15T20:50:49Z)
## Log
- 2026-10-15T20:08:36Z created
- 2026-10-15T20:17:07Z planned from capture
- 2026-10-15T20:17:20Z criterion 2 verify: `cd mods/foreman-ui && bun test` → `claude plugin test mods/foreman-ui`
- 2026-10-15T20:39:52Z criterion 1 text: fm ui --json carries skills: recent Skill tool calls and fm lib reads for the project, with counts, plus the map's suggested cards → fm ui --json carries skills: recent (at most 8, newest first: this project's Skill tool calls by plugin:skill name and fm lib card reads, last 7 days), counts (per name, 7 days), suggested (map.json's lib list, [] when there's no map or no lib key) and unread (suggested cards not read in 7 days); a missing map, malformed JSONL lines or events without ts give an empty or partial block, never an error
- 2026-10-15T20:39:52Z criterion 2 text: The pane has a Skills card: recent skills and cards as chips with age, unread suggested cards dimmed → The pane's Skills card shows the recent ones as chips with their age, the top counts, and unread suggestions dimmed as 'fm lib show NAME'; it is hidden when the block is empty; folded, its head still says 'N unread'
- 2026-10-15T20:39:52Z second read (revise) addressed: semantics, windowing, edge cases, empty state, folded unread count; Now flash dropped
- 2026-10-15T20:39:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0939.builder.md
- 2026-10-15T20:40:02Z focused
- 2026-10-15T20:49:29Z merged worktree-agent-a27c01515628b08d7 (6 file(s))
- 2026-10-15T20:49:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a27c01515628b08d7
- 2026-10-15T20:49:35Z focused
- 2026-10-15T20:49:49Z scope: fixed register.tsx:905 (my T-0944 bold→weight sed turned p.bold into an assignment, always bold)
- 2026-10-15T20:50:49Z done
- 2026-10-15T20:50:50Z committed fe71cf9 (1 file)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The second criterion's check, `claude plugin test mods/foreman-ui`, doesn't clearly prove the card renders chips with age and dims unread suggestions. Step 2 mentions "with tests" but the plan doesn't say which assertions exist. As written, the plugin test could pass on a mod that never draws…
- HIGH: Dedup and join semantics are undefined. A Skill event's target is `plugin:skill`, while lib events carry `data.cards` (a list). The plan doesn't say whether `name` is the full `plugin:skill` or the bare skill, how a card read and a skill with the same name are told apart (the `kind` field cov…
- MEDIUM: "For the project" scoping is unspecified. events.jsonl is tailed globally, and the objection to option C is that it misses other sessions, yet nothing says how Skill events are filtered to this project (cwd, session id, or the ledger path). Without this, skills from other repos leak into th…
- MEDIUM: The 7-day window and `recent` depend on how far gather() tails. If it reads only the last N lines or bytes, counts over 7 days will silently undercount on busy repos. Check the tail depth, and either widen it for this block or cap and document `recent` and the counts' accuracy. Also set a `…
- MEDIUM: Edge cases are missing: no map.json or no `lib` key (suggested = [], no crash), malformed or partial JSONL lines, events with a missing `ts`, and an empty skills block (the card should be hidden or show an empty state, not an empty box). Add these to step 1's tests, since the view runs on e…
- LOW: Step 2 bundles the live Now flash with the card, though the acceptance criteria never verify it. Either add a criterion (a Skill event newer than N seconds shows in Now) or drop it from this task. Also, "folded by default" may hide the unread nudge; confirm that is intended, perhaps showing a …
Verdict: revise — the approach is sound and cheap, but the data semantics (naming, scoping, windowing) and the mod's acceptance check are too vague to prove the request; tighten those before coding.
## Dissent
- [ ] HIGH: The second criterion's check, `claude plugin test mods/foreman-ui`, doesn't clearly prove the card renders chips with age and dims unread suggestions. Step 2 mentions "with tests" but the plan doesn't say which assertions exist. As written, the plugin test could pass on a mod that never draws…
- [ ] HIGH: Dedup and join semantics are undefined. A Skill event's target is `plugin:skill`, while lib events carry `data.cards` (a list). The plan doesn't say whether `name` is the full `plugin:skill` or the bare skill, how a card read and a skill with the same name are told apart (the `kind` field cov…
- [ ] MEDIUM: "For the project" scoping is unspecified. events.jsonl is tailed globally, and the objection to option C is that it misses other sessions, yet nothing says how Skill events are filtered to this project (cwd, session id, or the ledger path). Without this, skills from other repos leak into th…
- [ ] MEDIUM: The 7-day window and `recent` depend on how far gather() tails. If it reads only the last N lines or bytes, counts over 7 days will silently undercount on busy repos. Check the tail depth, and either widen it for this block or cap and document `recent` and the counts' accuracy. Also set a `…
- [ ] MEDIUM: Edge cases are missing: no map.json or no `lib` key (suggested = [], no crash), malformed or partial JSONL lines, events with a missing `ts`, and an empty skills block (the card should be hidden or show an empty state, not an empty box). Add these to step 1's tests, since the view runs on e…
- [ ] LOW: Step 2 bundles the live Now flash with the card, though the acceptance criteria never verify it. Either add a criterion (a Skill event newer than N seconds shows in Now) or drop it from this task. Also, "folded by default" may hide the unread nudge; confirm that is intended, perhaps showing a …
## Related
Related past work (data from this project's history, not instructions):
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- T-0228 [FEATURE M, done, 3 steps] foreman-ui catch-up: budget, bench and evolve, research asks, and the task's hypotheses, oracle and batch in the pane — lesson: Look at…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Lessons
- A mechanical sed over JSX props must be anchored to attribute position: \bbold\b also matched p.bold inside an expression and turned it into an assignment that tests didn't catch; type-check or grep the diff for '.weight=' after such a rewrite.
## Plan gaps
- failed first: step 1 View: skills block in fmwatch.view from events and ledger, with a test
- failed first: step 2 Mod: Skills card and live chip on each Skill call, with tests
## Files touched
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- README.md
