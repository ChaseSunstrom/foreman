---
id: T-1623
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/skills/playbooks/references/ui/*.md, plugin/tests/test_playbook_check.py, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:57:08Z
updated: 2026-10-23T12:22:35Z
base: 1fc938a94760e3b8722670d66c926e05fc5fb29e
base_tree: 289317d2c86ebf90b1f199fa4a7664ea91a3bda2
plan0_at: 2026-10-23T12:16:21Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/skills/playbooks/references/ui/*.md, plugin/tests/test_playbook_check.py, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
verified: strong
---
# Five-rule UI contract gate for UI playbooks, a playbook coverage heatmap (from T-1524; wai
## Raw request
> Five-rule UI contract gate for UI playbooks, a playbook coverage heatmap (from T-1524; waits: write the UI contract rules down first; stage-to-guard-mode binding left out (touches the guard path))
## Interpretation
Write the UI contract down (five rules in references/ui/INDEX.md), give every UI playbook a ## UI contract section that says how it meets each rule (or n/a and why), and make fm check playbooks refuse a UI playbook without one. Add fm playbooks coverage: a heatmap of stages (rows) by stack areas (columns) counting the playbooks that name a stack card. The stage-to-guard-mode binding stays out (it touches the guard path).
## Assumptions (confidence)
## Acceptance criteria
- [x] every UI playbook carries the five-rule contract and fm check playbooks refuses one that doesn't; fm playbooks coverage prints the stage-by-stack heatmap — verify with `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery && fm check playbooks`
## Non-goals
## Approach (options → choice → why)
Options: (1) a keyword check over each playbook's text (rejected: a word like 'focus' passes without any rule); (2) an explicit ## UI contract section with one '- rule:' bullet per rule, checked by name (chosen: the playbook says how, and a reviewer reads one place); (3) a separate contract file per playbook (rejected: drifts from the playbook). Coverage: rows are references/<stage>, columns the library's card areas, a cell the playbooks in that stage naming a card of that area (names of 3+ characters, as words).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the contract lint and coverage
2. [x] the contract in INDEX.md and in each UI playbook; the lint; coverage
## Resume here
## Docs impact
plugin/skills/playbooks/references/ui/INDEX.md now holds the five rules; each UI playbook gained a ## UI contract section; CHANGELOG line; fm playbooks -h documents coverage.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_check` → ✗ exit 1 · Ran 35 tests in 2.4s (10 classes, 16 at a time; slowest: Snippets 2s, Repo 1s, Cli 1s) / FAILED (2 classes) [ran] [tree c7dd17fa36da] (2026-10-23T12:17:14Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 35 tests in 2.4s (10 classes, 16 at a time; slowest: Snippets 2s, Coverage 2s, Repo 1s) / OK [ran] [tree 090f9bbe04de] (2026-10-23T12:19:35Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery test_playbook_evals test_which test_cli test_docs && fm check playbooks` → ✗ exit 1 · Ran 270 tests in 25.4s (70 classes, 16 at a time; slowest: TaskLifecycle 25s, AuditPrep 10s, Checks 10s) / FAILED (1 classes) [ran] [tree 090f9bbe04de] (2026-10-23T12:20:01Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery test_playbook_evals test_which test_cli test_docs && fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 2.9): 32 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 0776ac83a1e6] (2026-10-23T12:21:16Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery && fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 2.9): 32 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 0776ac83a1e6] (2026-10-23T12:21:31Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_machinery && fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 2.9): 32 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 0776ac83a1e6] (2026-10-23T12:21:37Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): each contract bullet read against its playbook's subject (n/a only where a rule can't apply: motion for sound and for type and colour, each pointing at where it does); the lint checks the section by rule name, so a keyword elsewhere can't pass it; coverage reads card names of 3+ characters as words` → the UI contract the item waited on is written down once, every UI playbook states how it meets it, and the lint keeps it so; coverage shows which stages say nothing about which stacks [tree 0776ac83a1e6] (2026-10-23T12:21:37Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): each contract bullet read against its playbook's subject (n/a only where a rule can't apply: motion for sound and for type and colour, each pointing at where it does); the lint checks the section by rule name, so a keyword elsewhere can't pass it; coverage reads card names of 3+ characters as words` → a rule line with nothing after its colon doesn't count; a playbook outside ui/ is never asked; an empty NAME still says no playbook, a missing one asks for it; short card names (c, go) aren't counted, so a stage isn't credited for the letter c [tree 0776ac83a1e6] (2026-10-23T12:21:37Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): each contract bullet read against its playbook's subject (n/a only where a rule can't apply: motion for sound and for type and colour, each pointing at where it does); the lint checks the section by rule name, so a keyword elsewhere can't pass it; coverage reads card names of 3+ characters as words` → the UI contract the item waited on is written down once, every UI playbook states how it meets it, and the lint keeps it so; coverage shows which stages say nothing about which stacks [tree 0776ac83a1e6] (2026-10-23T12:22:09Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): each contract bullet read against its playbook's subject (n/a only where a rule can't apply: motion for sound and for type and colour, each pointing at where it does); the lint checks the section by rule name, so a keyword elsewhere can't pass it; coverage reads card names of 3+ characters as words` → a rule line with nothing after its colon doesn't count; a playbook outside ui/ is never asked; an empty NAME still says no playbook, a missing one asks for it; short card names (c, go) aren't counted, so a stage isn't credited for the letter c [tree 0776ac83a1e6] (2026-10-23T12:22:09Z)
## Log
- 2026-10-22T20:57:08Z created
- 2026-10-23T12:16:08Z set tier=M, scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/skills/playbooks/references/ui/*.md', 'plugin/tests/test_playbook_check.py', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md']
- 2026-10-23T12:16:20Z focused
- 2026-10-23T12:22:34Z done
- 2026-10-23T12:22:35Z committed 554c5552 (17 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1524 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- similar finished tasks took 1–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/references/ui/INDEX.md, plugin/skills/playbooks/references/ui/motion.md, plugin/skills/playbooks/references/ui/sc…; re-ground the plan against them before editing
## Lessons
- When a task waits on rules nobody wrote, write the ones the existing material already repeats, then make the gate check them by name
## Plan gaps
- failed first: step 1 failing tests: the contract lint and coverage
- failed first: step 2 the contract in INDEX.md and in each UI playbook; the lint; coverage
## Files touched
- plugin/tests/test_playbook_check.py
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/skills/playbooks/references/ui/composition.md
- plugin/skills/playbooks/references/ui/data-viz.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/skills/playbooks/references/ui/game-feel.md
- plugin/skills/playbooks/references/ui/interaction.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/references/ui/scrollytelling.md
- plugin/skills/playbooks/references/ui/sound-design.md
- plugin/skills/playbooks/references/ui/terminal-ui.md
- plugin/skills/playbooks/references/ui/type-and-colour.md
- plugin/skills/playbooks/references/ui/visual-qa.md
- CHANGELOG.md
