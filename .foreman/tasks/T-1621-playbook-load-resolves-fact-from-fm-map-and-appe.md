---
id: T-1621
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmmap.py, plugin/tests/test_playbook_machinery.py, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/skills/playbooks/SKILL.md, MASTER.md, plugin/skills/playbooks/references/verify/verification-loop.md, plugin/lib/fmcore.py]
depends_on: []
source: user
created: 2026-10-22T20:57:01Z
updated: 2026-10-22T22:03:36Z
base: 58e647f6ea6f34d7ca25820626b2acc32d75e57f
base_tree: 0b7fc7ed1d7b8d3b5c70190590c80f6ecec86dcb
plan0_at: 2026-10-22T21:30:52Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmmap.py, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
verified: strong
---
# Playbook load resolves {{fact}} from fm map and appends a project's .foreman/playbooks overlays
## Raw request
> Playbook load resolves {{fact}} from fm map and appends a project's .foreman/playbooks overlays
## Interpretation
When a playbook loads through fm (fm playbooks show NAME, which the playbooks skill uses), {{fact}} placeholders resolve from fm map's facts for the current project (test command, language, entry points…); an unknown fact stays visible as {{fact?}}. A project's .foreman/playbooks/NAME.md overlay is appended after the shipped text under a 'This project' heading. It works from Claude Code because the skill reads playbooks through fm.
## Assumptions (confidence)
## Acceptance criteria
- [x] overlay text follows the shipped playbook and {{fact}} resolves, an unknown fact left visible — verify with `python3 plugin/tests/run.py test_playbook_machinery.Load`
## Non-goals
## Approach (options → choice → why)
Options: render copies at install time (go stale, many files); let Claude substitute facts by reading fm map itself (costs tokens every load, inconsistent); resolve at load in fmplaybooks. Choice: resolve at load: facts stay current, nothing generated is stored. Overlays are plain Markdown read only from the project's .foreman folder and capped in size, never executed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a fixture project and overlay
2. [x] load function reading fm map facts
3. [x] hook into the playbook load path and fm playbooks show
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery.Load` → ✗ exit 1 · Ran 9 tests in 1.8s (1 classes, 16 at a time; slowest: Load 2s) / FAILED (1 classes) [ran] [tree 5e2bdf8373d3] (2026-10-22T21:36:41Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_machinery.Load` → exit 0 · Ran 9 tests in 3.1s (1 classes, 16 at a time; slowest: Load 3s) / OK [ran] [tree 13223f73ace4] (2026-10-22T21:38:27Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost test_help test_cli test_docs test_firstrun test_map test_doctor 2>&1 | tail -25` → exit 0 · Ran 300 tests in 30.5s (87 classes, 16 at a time; slowest: TaskLifecycle 30s, TaskCostCap 15s, StateViews 15s) / OK [ran] [tree 13223f73ace4] (2026-10-22T21:39:00Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost` → exit 0 · Ran 57 tests in 6.4s (17 classes, 16 at a time; slowest: TaskCostCap 6s, Load 3s, Snippets 2s) / OK [ran] [tree 4cebd25a4393] (2026-10-22T21:40:07Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost` → exit 0 · Ran 60 tests in 6.5s (18 classes, 16 at a time; slowest: TaskCostCap 6s, Load 3s, Snippets 2s) / OK [ran] [tree 381ebdde4de2] (2026-10-22T21:43:13Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery.Load` → exit 0 · Ran 9 tests in 2.8s (1 classes, 16 at a time; slowest: Load 3s) / OK [ran] [tree 381ebdde4de2] (2026-10-22T21:43:19Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery.Load` → ✗ exit 1 · Ran 13 tests in 6.2s (1 classes, 16 at a time; slowest: Load 6s) / FAILED (1 classes) [ran] [tree d0ec2f266bd7] (2026-10-22T21:50:10Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost test_core` → exit 0 · Ran 134 tests in 12.9s (35 classes, 16 at a time; slowest: TaskCostCap 13s, Load 9s, Repo 3s) / OK [ran] [tree ce1a8f73925e] (2026-10-22T21:52:41Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost test_core` → exit 0 · Ran 134 tests in 15.6s (35 classes, 16 at a time; slowest: TaskCostCap 15s, Load 10s, Repo 4s) / OK [ran] [tree d18e0a5db9ab] (2026-10-22T21:53:58Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_machinery.Load` → exit 0 · Ran 13 tests in 7.1s (1 classes, 16 at a time; slowest: Load 7s) / OK [ran] [tree 4ca76f00c99c] (2026-10-22T22:02:07Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_machinery test_playbook_check test_cost test_core test_code_tui` → exit 0 · Ran 308 tests in 15.1s (59 classes, 16 at a time; slowest: Fuzz 14s, Command 13s, TaskCostCap 12s) / OK [ran] [tree 4ca76f00c99c] (2026-10-22T22:02:23Z)
- (step 3) `fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 6.6): 35 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 4ca76f00c99c] (2026-10-22T22:02:26Z)
- (audit adversary) `overlay under a provenance heading, every line blockquoted so it can't form headings, marked (uncommitted) when not in git; links refused, 16 KB cap, invisible selectors dropped; repo-derived facts as inline code, capped` → hostile overlay tested [tree 4ca76f00c99c] (2026-10-22T22:02:27Z)
- (audit edge) `facts render only in the shipped text; Go/Actions/Handlebars placeholders untouched; the test-command fallback ignores tests/` → tested [tree 4ca76f00c99c] (2026-10-22T22:02:28Z)
- (audit operator) `fm playbooks show NAME; workers may run it; an old .foreman/playbooks folder gets a pointer` → tested [tree 4ca76f00c99c] (2026-10-22T22:02:28Z)
- (audit maintainer) `SKILL.md 9,714 chars with headroom; verification-loop uses {{test}} within the ratchet` → fm check playbooks: 0 problems [tree 4ca76f00c99c] (2026-10-22T22:02:29Z)
- (audit intent) `criterion: overlay follows the shipped text, {{fact}} resolves, unknown stays visible; overlays at .claude/playbooks by decision` → met (13 tests) [tree 4ca76f00c99c] (2026-10-22T22:02:29Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_machinery.Load` → exit 0 · Ran 13 tests in 6.9s (1 classes, 16 at a time; slowest: Load 7s) / OK [ran] [tree 4ca76f00c99c] (2026-10-22T22:02:44Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → overlays fenced as quoted project notes, can't pose as shipped rules [tree 4ca76f00c99c] (2026-10-22T22:02:44Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → facts only in shipped text [tree 4ca76f00c99c] (2026-10-22T22:02:44Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met; overlays at .claude/playbooks by decision [tree 4ca76f00c99c] (2026-10-22T22:02:44Z)
## Log
- 2026-10-22T20:57:01Z created
- 2026-10-22T20:57:02Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmmap.py', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md']
- 2026-10-22T20:57:03Z split from T-1524 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:49Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_playbook_machinery.Load`
- 2026-10-22T21:30:13Z criterion 1 text: overlay text follows the shipped playbook and {{fact}} resolves, an unknown fact left visible — verify with python3 plugin/tests/run.py test_playbook_machinery.Load → overlay text follows the shipped playbook and {{fact}} resolves, an unknown fact left visible
- 2026-10-22T21:30:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1621.builder.md
- 2026-10-22T21:30:52Z focused
- 2026-10-22T21:38:00Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmmap.py', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/lib/fmcost.py', 'plugin/skills/playbooks/SKILL.md', 'MASTER.md']
- 2026-10-22T21:38:05Z scope widened: fmcli registers the fm playbooks verb, fmcost counts a show as a playbook read in fm usage, SKILL.md routes loads through fm, MASTER.md one line
- 2026-10-22T21:43:06Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmmap.py', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/lib/fmcost.py', 'plugin/skills/playbooks/SKILL.md', 'MASTER.md', 'plugin/skills/playbooks/references/verify/verification-loop.md']
- 2026-10-22T21:43:07Z steer: ANDON resolved by the coordinator: overlays move to .claude/playbooks (guard allows writes there), guard test added, {{test}} in verification-loop, playbooks show in WORKER_SUBREADS
- 2026-10-22T21:52:27Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmmap.py', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/lib/fmcost.py', 'plugin/skills/playbooks/SKILL.md', 'MASTER.md', 'plugin/skills/playbooks/references/verify/verification-loop.md', 'plugin/lib/fmcore.py']
- 2026-10-22T21:52:27Z steer: review fixes: overlay blockquoted under a provenance line and marked (uncommitted); facts only in shipped text; repo facts as inline code ≤120; test fallback (?:^|\s)test; plain() drops variation selectors; broken map → one stderr note; .foreman/playbooks named; SKILL index lines point at fm playbooks show
- 2026-10-22T22:01:47Z merged worktree-agent-ae138b07150d9d229 (9 file(s))
- 2026-10-22T22:01:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae138b07150d9d229
- 2026-10-22T22:01:49Z focused
- 2026-10-22T22:02:30Z scope: fmcore.plain (drops variation selectors everywhere, per review), MASTER.md, SKILL.md, verification-loop.md ({{test}}), fmcli WORKER_SUBREADS
- 2026-10-22T22:03:36Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1524 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- playbook Living Docs Governance (skills/playbooks/references/context/living-docs.md)
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- likely tests for the scope: plugin/tests/test_map.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/SKILL.md, plugin/skills/playbooks/references/verify/verifi…; re-ground the plan against them before editing
## Why not caught
the first overlay design appended plain Markdown under a heading
## Lessons
- Repo-supplied text spliced into instructions must be fenced and labelled with where it came from, or it reads as the instructions themselves
## Plan gaps
- failed first: step 1 failing test with a fixture project and overlay
## Files touched
- plugin/tests/test_playbook_machinery.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/skills/playbooks/SKILL.md
- MASTER.md
- ANDON.md
- CHANGELOG.md
- plugin/skills/playbooks/references/verify/verification-loop.md
- plugin/lib/fmcore.py
