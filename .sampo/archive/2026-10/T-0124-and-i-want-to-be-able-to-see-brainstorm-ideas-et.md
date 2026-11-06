---
id: T-0124
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:14:20Z
updated: 2026-10-03T05:33:40Z
base: e371c8ea24827f0293c49a54aa949317aab8058d
base_tree: c456ea8dd85ddafb92295236f08ac8e94c180cec
verified: strong
---
# See brainstorms in the dashboard: live progress while fm ideas runs, then the ideas
## Raw request
> and I want to be able to see brainstorm ideas, etc. subagents working, etc. also what is the inbox?
## Interpretation
User: I want to see brainstorm ideas and subagents working. Subagents already show (card, mini Claudes, quiet time); brainstorms run as tool-less claude -p children inside one long Bash call and show nothing until the end.
## Assumptions (confidence)
## Acceptance criteria
- [x] view has the newest brainstorm, running or done — verify with `python3 plugin/tests/run.py -p test_ui.py`
- [x] pane shows a Brainstorm card — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm ideas writes status.json (lenses, rounds, start) into its folder; fm ui --json reports the newest brainstorm (running: answers in so far and ideas found; done: count and the newest ideas); the pane draws a Brainstorm card; (b) stream progress through events. Choice (a): the folder already fills one file per lens as children finish, so a status file plus a directory count is the whole mechanism; the mod's 2 s poll picks it up.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (python + mod)
2. [x] status.json + view
3. [x] pane card, docs
## Resume here
## Docs impact
CHANGELOG.md: brainstorm visibility
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 40 tests across 1 file. [1.87s] [ran] [tree 3b1981469c23] (2026-10-03T05:32:11Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 40 tests across 1 file. [1.91s] [ran] [tree 3b1981469c23] (2026-10-03T05:32:14Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 40 tests across 1 file. [1.84s] [ran] [tree 3b1981469c23] (2026-10-03T05:32:16Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ui.py` → exit 0 · Ran 10 tests in 4.0s (1 classes, 16 at a time; slowest: UiView 4s) / OK [ran] [tree 3b1981469c23] (2026-10-03T05:32:20Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ui.py` → exit 0 · Ran 10 tests in 6.1s (1 classes, 16 at a time; slowest: UiView 6s) / OK [ran] [tree 699bd2f47c7d] (2026-10-03T05:33:40Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 40 tests across 1 file. [3.16s] [ran] [tree 699bd2f47c7d] (2026-10-03T05:33:40Z)
- (audit intent) `self-review; python + mod tests; validate; tsc` → brainstorms visible in the chat (running fm ideas row) and the pane; subagents were already visible (card, minis, quiet time) [tree 699bd2f47c7d] (2026-10-03T05:33:40Z)
- (audit edge) `self-review; python + mod tests; validate; tsc` → no brainstorm → none; a run that never finished counts as stopped after an hour; ideas deduped; the running folder joins the watch list so progress updates as each lens answers [tree 699bd2f47c7d] (2026-10-03T05:33:40Z)
## Log
- 2026-10-03T04:14:20Z created
- 2026-10-03T05:29:44Z planned from capture
- 2026-10-03T05:29:44Z focused
- 2026-10-03T05:31:12Z steer: the user wants things in the chat, not the right panel: the running fm ideas row shows the brainstorm's progress inline
- 2026-10-03T05:33:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- T-0109 [FEATURE M, done, 3 steps] Background shells visible; mascot drawn like Claude Code's Clawd; mini colored Claudes per subagent — lesson: Mods: module variables re…
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- similar finished tasks took 3–8 steps
## Lessons
- Show long-running work where the person is looking: the chat row of the call doing it
## Files touched
- plugin/lib/fmideas.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/tests/test_ui.py
