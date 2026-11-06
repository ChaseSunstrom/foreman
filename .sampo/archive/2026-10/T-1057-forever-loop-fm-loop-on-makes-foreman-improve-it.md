---
id: T-1057
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T04:31:53Z
base: f896182d03c79cb50fa2b8e11036af4050e1dde4
base_tree: 33137fa4757aeb3ec4e3773a9f6221ef1ac62c3f
verified: strong
---
# Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo
## Raw request
> FEATURE: Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbox are empty, fm next runs a round (review what shipped since the last round, a brainstorm probe past every earlier ideas.md, ground, intake the slate, build it), and stops only on a dry run twice in a row, the budget, or the user (fm loop off); the pane and band show the round
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
The user wants Foreman to keep improving itself without being asked: when there is no work left, it should start the next improvement round on its own (review what shipped, brainstorm on top of it past every earlier idea, ground the ideas, queue the good ones, build them) and keep going round after round, stopping only when rounds stop producing anything of value, when the budget says so, or when the user turns it off. It must be Foreman enforcing it (fm next and the Stop drive), not a habit the agent has to remember.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm loop on makes an empty queue start a round (fm next names it, the drive continues into it), fm loop yield counts dry rounds and two in a row stop the loop with a recorded decision, and fm ui and the pane show the loop — verify with `python3 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
A complete version: fm loop on|off|status (meta: on, round, dry streak, started, last round, stop reason); fm loop round prints the round's brief (what shipped since the last round: closed tasks and commits; the exact fm mission + fm ideas line run past every earlier ideas.md; ground, intake, then fm loop yield N) and marks it started; fm loop yield N records the grounded yield, fewer than 3 is dry, two dry rounds in a row turn the loop off with an fm decide record; fm next, with the queue and inbox empty and the loop on, names the round as the next action; the Stop hook's drive continues into the round on every drain (not once), waiting while usage runs ahead of pace and within DRIVE_MAX; fm ui carries loop state and the pane head and band show it (∞ round K). Options: (a) fmloop module wired into fm next and the drive (enforced by Foreman, works in any session); (b) Claude Code's /loop or ScheduleWakeup (needs the user to type a slash command, per session, no dry-run stop); (c) a skill with the procedure only (relies on the agent remembering: what the user asked us to stop relying on). Choice (a); headless fm run --loop is captured as a follow-up.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fm loop on/off/status, round brief (shipped since, ideas line with --seen), yield and the dry stop, fm next stage, the drive's continuation
2. [x] fmloop module and fm loop command; fm next and the Stop drive wired to it
3. [x] fm ui loop state; pane head and band show the round; README, MASTER, rules
## Resume here
T-1090: planning only (turn.step tap per agentId → said map; liveTree narration rows; divider above the tree); back to T-1057 review fixes
<!-- auto -->
- 2026-10-16T04:28:44Z step 1/3: Failing tests: fm loop on/off/status, round brief (shipped since, ideas line with --seen), yield and the dry stop, fm next stage, the drive's continuation
- git: foreman/build; 13 uncommitted: CHANGELOG.md, MASTER.md, README.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmwatch.py
- touched since last checkpoint: plugin/lib/fmloop.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_loop.py, plugin/lib/fmwatch.py, plugin/lib/fmhooks.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md, MASTER.md, README.md, plugin/rules/foreman.md
## Docs impact
README forever loop paragraph; MASTER fmloop entry; rules plain-words line; CHANGELOG; fm help tiers
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_loop` → ✗ exit 1 · Ran 6 tests in 1.0s (2 classes, 16 at a time; slowest: Loop 1s, PipeProgramDebris 0s) / FAILED (1 classes) [ran] [tree f4f0cc9b0f68] (2026-10-16T04:11:24Z)
- (step 2) `python3 plugin/tests/run.py test_loop test_hooks test_cli` → exit 0 · Ran 259 tests in 68.6s (50 classes, 16 at a time; slowest: Stop 69s, TaskLifecycle 53s, PreToolUse 48s) / OK [ran] [tree b2587db9fb49] (2026-10-16T04:26:04Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 113 tests across 1 file. [10.30s] [ran] [tree fa6641c01533] (2026-10-16T04:27:02Z)
- (ac 1) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 12 tests in 3.1s (3 classes, 16 at a time; slowest: Loop 3s, LoopReview 2s, PipeProgramDebris 0s) / OK [ran] [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (step 1) `python3 plugin/tests/run.py test_loop test_hooks test_cli test_help` → exit 0 · Ran 268 tests in 39.2s (52 classes, 16 at a time; slowest: Stop 39s, TaskLifecycle 27s, PreToolUse 23s) / OK [ran] [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1057-review): 7 findings fixed test-first (6 regression tests red then green); intent/edge/maintainer changes-needed items all closed` → an empty queue with the loop on starts the next round from fm next and the Stop drive; the dry stop is Foreman's count, not the model's memory [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1057-review): 7 findings fixed test-first (6 regression tests red then green); intent/edge/maintainer changes-needed items all closed` → no new trust boundary; titles in the round brief are the user's own data; seen paths shell-quoted [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1057-review): 7 findings fixed test-first (6 regression tests red then green); intent/edge/maintainer changes-needed items all closed` → no git, a GIT_DIR, unreadable times, a double yield, yield before a round, usage ahead of pace (pauses) [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1057-review): 7 findings fixed test-first (6 regression tests red then green); intent/edge/maintainer changes-needed items all closed` → fm loop status shows round and dry streak; the pane and band show ∞ round N; README, MASTER, rules, CHANGELOG, fm help [tree e1c6459ab122] (2026-10-16T04:31:51Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1057-review): 7 findings fixed test-first (6 regression tests red then green); intent/edge/maintainer changes-needed items all closed` → one fmloop module; fm next and the drive call it; the drive cap resets on progress only while looping [tree e1c6459ab122] (2026-10-16T04:31:51Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:10:00Z set tier=M
- 2026-10-16T04:10:14Z focused
- 2026-10-16T04:11:48Z paused: focus moved to T-1035
- 2026-10-16T04:23:31Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T04:23:31Z focused
- 2026-10-16T04:28:45Z focused
- 2026-10-16T04:31:52Z done
- 2026-10-16T04:31:53Z committed 158bf06 (13 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261015-215750: Request: how can we make it so worktree agents can easily resumed if a session was stopped or something? etc. and super improve recursi…
- research mission-20261014-130857: Request: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integ…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
## Lessons
- An invariant that ends a loop must be counted by the harness itself (tasks made since the round began), never left to the agent remembering a command
## Plan gaps
- failed first: step 1 Failing tests: fm loop on/off/status, round brief (shipped since, ideas line with --seen), yield an…
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmloop.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmwatch.py
- plugin/lib/fmhooks.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/rules/foreman.md
- demo/live.cast
- demo/live.mp4
- demo/live.svg
