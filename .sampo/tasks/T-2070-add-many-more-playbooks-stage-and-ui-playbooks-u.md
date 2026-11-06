---
id: T-2070
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T00:49:21Z
updated: 2026-10-31T01:07:54Z
base: db3757997a4165cc1e75d8275d64384696b07a72
base_tree: d19f6c4d4cfdd4a780a13372873280f4777a02c5
plan0_at: 2026-10-31T00:22:40Z
plan0_scope: []
verified: strong
---
# Add many more playbooks (stage and UI playbooks under plugin/skills/playbooks), each…
## Raw request
> FEATURE: add many more playbooks (stage and UI playbooks under plugin/skills/playbooks), each grounded, indexed and linted
## Interpretation
The user's ask: many more playbooks under plugin/skills/playbooks, each grounded, indexed and linted. Grounding: 90 playbooks across 16 stages; fm playbooks coverage shows whole stack columns with no playbook in any stage (claude-code, data, games, go, hardware, mobile, native and others) and most stages with one or none per stack.
## Assumptions (confidence)
## Acceptance criteria
- [x] at least 20 new playbooks fill the most-hit empty (stage, stack) cells in fm playbooks coverage; each names its stack cards, is in the index and routes, and passes the playbook lint — verify with `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery`
## Non-goals
## Approach (options → choice → why)
Options: (1) fill the coverage holes that real work hits: rank (stage, stack) pairs by how often this machine's tasks touched that stack in that stage (fm recall and task history), and write one playbook per top empty pair, each naming its stack cards and verify commands; (2) mine done tasks with fm playbooks draft ID (good for repeats, thin for stacks never worked); (3) one generic playbook per stack (breadth without stage fit). Choice: 1 for the ranked holes, with 2 where a done task already shows the procedure. Each new playbook passes test_playbook_check (its lint) and appears in the stage index and fm playbooks route; a held-out fm playbooks eval runs on a sample at the end-of-run exam, not per playbook.
## Risks and rollback
## Execution prompt
## Steps
1. [x] rank empty (stage, stack) pairs by task history; pick the top 20+
2. [x] write each (fm playbooks draft where a done task shows it), lint, index, route
3. [x] coverage before and after, docs (README playbook count, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-31T00:28:09Z step 2/3: write each (fm playbooks draft where a done task shows it), lint, index, route
- git: worktree-agent-adb9830da5bb4b631; 32 uncommitted: plugin/skills/playbooks/SKILL.md, plugin/skills/playbooks/references/build/INDEX.md, plugin/skills/playbooks/references/context/INDEX.md, plugin/skills/playbooks/references/ops/INDEX.md, plugin/skills/playbooks/references/perf/INDEX.md, plugin/skills/playbooks/references/release/INDEX.md, plugin/skills/playbooks/references/security/INDEX.md, plugin/skills/playbooks/references/build/embedded-build.md, plugin/skills/playbooks/references/build/game-build.md, plugin/skills/playbooks/references/build/mobile-build.md
- touched since last checkpoint: plugin/skills/playbooks/references/build/mobile-build.md, plugin/skills/playbooks/references/build/game-build.md, plugin/skills/playbooks/references/fix/data-pipeline.md, plugin/skills/playbooks/references/fix/serial-and-bus.md, plugin/skills/playbooks/references/verify/plugin-checks.md, plugin/skills/playbooks/references/verify/data-quality.md, plugin/skills/playbooks/references/verify/game-logic.md, plugin/skills/playbooks/references/verify/go-checks.md, plugin/skills/playbooks/references/verify/mobile-tests.md, plugin/skills/playbooks/references/perf/game-frame-budget.md, plugin/skills/playbooks/references/perf/go-profiling.md, plugin/skills/playbooks/references/perf/data-queries.md, plugin/skills/playbooks/references/perf/mobile-startup.md, plugin/skills/playbooks/references/ops/data-pipeline-incident.md, plugin/skills/playbooks/references/ops/device-fleet.md
## Docs impact
CHANGELOG Unreleased, plugin/skills/playbooks/SKILL.md, the stage INDEX files
## Verification evidence
- (step 1) `fm playbooks coverage` → exit 0 · verify    · ░ ▒ · · ▒ · · · · · · · · ▓ · · · · ▒ · · ░ · ░ ▓ ▓ · ▒ / playbooks in a stage naming a card of that stack: · none  ░ 1  ▒ 2  ▓ 3  █ 4+ [ran] [tree 52e600a5373e] (2026-10-31T00:23:42Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 4.2s (17 classes, 16 at a time; slowest: Load 4s, Coverage 3s, Snippets 2s) / OK [ran] [tree 114872bc00d0] (2026-10-31T00:31:48Z)
- (step 3) `fm playbooks coverage` → exit 0 · verify    · ░ ▒ · · ▒ · · · · · · · · ▓ · · · · ▒ · · ░ · ░ ▓ ▓ · ▒ / playbooks in a stage naming a card of that stack: · none  ░ 1  ▒ 2  ▓ 3  █ 4+ [ran] [tree 114872bc00d0] (2026-10-31T00:31:49Z)
- `fm check --affected (affected tests only): cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.45s] [ran] [tree 114872bc00d0] (2026-10-31T00:32:04Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 3.6s (17 classes, 16 at a time; slowest: Load 3s, Coverage 2s, Snippets 2s) / OK [ran] [tree b9164379a317] (2026-10-31T01:06:27Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 3.6s (17 classes, 16 at a time; slowest: Load 3s, Coverage 2s, Snippets 2s) / OK [ran] [tree b9164379a317] (2026-10-31T01:06:31Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 3.6s (17 classes, 16 at a time; slowest: Load 3s, Coverage 2s, Snippets 2s) / OK [ran] [tree b9164379a317] (2026-10-31T01:06:35Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 3.5s (17 classes, 16 at a time; slowest: Load 3s, Coverage 2s, Snippets 2s) / OK [ran] [tree b9164379a317] (2026-10-31T01:06:38Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_check test_playbook_route test_playbook_machinery` → exit 0 · Ran 86 tests in 3.6s (17 classes, 16 at a time; slowest: Load 3s, Coverage 2s, Snippets 2s) / OK [ran] [tree 942589248314] (2026-10-31T01:07:14Z)
- (audit intent) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW (a prod index example, a deprecated altool, a grep that always exits 0, a fixed /tmp path, a stale 'hooks' blurb) fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → 21 playbooks fill empty stage-by-stack cells, each naming its cards and real commands [tree 942589248314] (2026-10-31T01:07:14Z)
- (audit maintainer) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW (a prod index example, a deprecated altool, a grep that always exits 0, a fixed /tmp path, a stale 'hooks' blurb) fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → per-stage INDEX files keep SKILL.md under budget; the route test's held-out margin is one, noted [tree 942589248314] (2026-10-31T01:07:14Z)
- (audit adversary) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW (a prod index example, a deprecated altool, a grep that always exits 0, a fixed /tmp path, a stale 'hooks' blurb) fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → no playbook pipes a download into a shell, disables a guard, force-pushes, commits a secret or runs untrusted code unsandboxed; the plugin-security playbook the diff names was added and removed inside the lane and isn't in the tree; the eval output uses mktemp and the store key stays out of git [tree 942589248314] (2026-10-31T01:07:14Z)
- (audit intent) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → 21 playbooks fill empty stage-by-stack cells, each naming its cards and real commands [tree 942589248314] (2026-10-31T01:07:39Z)
- (audit maintainer) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → per-stage INDEX files keep SKILL.md under budget; the route test's held-out margin is one, noted [tree 942589248314] (2026-10-31T01:07:39Z)
- (audit adversary) `fm-reviewer intent+maintainer+adversary on the builder's branch: all 21 grounded in real cards, no routing lost, no unsafe instructions; 1 MEDIUM (dbt state:modified without --state/--target) and 5 LOW fixed in b3a5921c; playbook tests 86 green, fm check playbooks clean` → no playbook pipes a download into a shell, disables a guard, force-pushes, commits a secret or runs untrusted code unsandboxed; the plugin-security playbook the diff names was added and removed inside the lane; the eval output uses mktemp and the store key stays out of git [tree 942589248314] (2026-10-31T01:07:39Z)
## Log
- 2026-10-30T00:49:21Z created
- 2026-10-31T00:21:33Z planned: it has criteria and steps
- 2026-10-31T00:21:33Z set tier=M
- 2026-10-31T00:22:27Z set approved=True
- 2026-10-31T00:22:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2070.builder.md
- 2026-10-31T00:22:39Z focused
- 2026-10-31T01:06:22Z merged worktree-agent-adb9830da5bb4b631 (29 file(s))
- 2026-10-31T01:06:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adb9830da5bb4b631
- 2026-10-31T01:06:23Z focused
- 2026-10-31T01:07:53Z done
- 2026-10-31T01:07:54Z committed e786f31b (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Lessons
- The playbook lint checks shape, not commands: a reviewer reading the commands caught a dbt call that selects nothing and a grep check that always passes
## Files touched
- plugin/skills/playbooks/references/build/mobile-build.md
- plugin/skills/playbooks/references/build/embedded-build.md
- plugin/skills/playbooks/references/build/game-build.md
- plugin/skills/playbooks/references/fix/hook-failures.md
- plugin/skills/playbooks/references/fix/data-pipeline.md
- plugin/skills/playbooks/references/fix/mobile-crash.md
- plugin/skills/playbooks/references/fix/serial-and-bus.md
- plugin/skills/playbooks/references/verify/plugin-checks.md
- plugin/skills/playbooks/references/verify/data-quality.md
- plugin/skills/playbooks/references/verify/game-logic.md
- plugin/skills/playbooks/references/verify/go-checks.md
- plugin/skills/playbooks/references/verify/mobile-tests.md
- plugin/skills/playbooks/references/perf/game-frame-budget.md
- plugin/skills/playbooks/references/perf/go-profiling.md
- plugin/skills/playbooks/references/perf/data-queries.md
- plugin/skills/playbooks/references/perf/mobile-startup.md
- plugin/skills/playbooks/references/security/plugin-and-hook-security.md
- plugin/skills/playbooks/references/ops/data-pipeline-incident.md
- plugin/skills/playbooks/references/ops/device-fleet.md
- plugin/skills/playbooks/references/release/plugin-release.md
- plugin/skills/playbooks/references/release/mobile-store-release.md
- plugin/skills/playbooks/references/release/go-release.md
- plugin/skills/playbooks/references/context/instruction-files.md
- plugin/skills/playbooks/references/fix/INDEX.md
- plugin/skills/playbooks/references/verify/INDEX.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/build/INDEX.md
- plugin/skills/playbooks/references/context/INDEX.md
- plugin/skills/playbooks/references/ops/INDEX.md
- plugin/skills/playbooks/references/perf/INDEX.md
