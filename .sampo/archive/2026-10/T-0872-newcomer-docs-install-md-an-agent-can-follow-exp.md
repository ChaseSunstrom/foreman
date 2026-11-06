---
id: T-0872
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:11:38Z
updated: 2026-10-15T14:17:14Z
base: 427b8f473597cf0c1bb2760074f7d3aaaa241bf6
base_tree: 96b78ca30406402e8ed145635b06cbaedcd3ef92
verified: ok
---
# Newcomer docs: INSTALL.md an agent can follow (explain defaults, ask consent, install, fm doctor), README links it and gains 'When not to use Foreman'
## Raw request
> Newcomer docs: INSTALL.md an agent can follow (explain defaults, ask consent, install, fm doctor), README links it and gains 'When not to use Foreman'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] INSTALL.md exists with the consent steps and README links it and has a 'When not to use Foreman' section — verify with `test -s INSTALL.md && grep -q INSTALL.md README.md && grep -q 'When not to use Foreman' README.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Write INSTALL.md and the README sections
## Resume here
<!-- auto -->
- 2026-10-15T14:16:54Z steps 1/1 done
- git: foreman/build; 2 uncommitted: README.md, INSTALL.md
- touched since last checkpoint: INSTALL.md, README.md
## Docs impact
INSTALL.md (new), README
## Verification evidence
- (step 1) `test -s INSTALL.md && grep -q INSTALL.md README.md && grep -q 'When not to use Foreman' README.md` → exit 0 · (no output) [ran] [tree 6d76e790909e] (2026-10-15T14:15:25Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply; python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 14:14 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 14:08 UTC; claude pl [ran] [tree 6d76e790909e] (2026-10-15T14:16:48Z)
- (ac 1) `test -s INSTALL.md && grep -q INSTALL.md README.md && grep -q 'When not to use Foreman' README.md` → exit 0 · (no output) [ran] [tree 6d76e790909e] (2026-10-15T14:17:13Z)
- (audit self) `self: INSTALL.md walks an agent through reading install.sh, explaining each default in plain words (third-party plugins, the mod, ~/.claude wiring, the bypass question), asking, running, and checking with fm doctor; README links it and gains 'When not to use Foreman' (one-off jobs, native Windows, approve-every-command, tight budgets, code that must not leave the machine)` → no findings [tree 6d76e790909e] (2026-10-15T14:17:13Z)
## Log
- 2026-10-15T14:11:38Z created
- 2026-10-15T14:14:52Z focused
- 2026-10-15T14:16:55Z paused: focus moved to T-0873
- 2026-10-15T14:17:12Z focused
- 2026-10-15T14:17:13Z done
- 2026-10-15T14:17:14Z committed 7f13f69 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- playbook Living Docs Governance (skills/playbooks/references/context/living-docs.md)
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
- the similar finished task took 5 steps
## Lessons
- Agents install plugins for people now: a guide written for the agent carries the consent steps a curl one-liner skips
## Files touched
- INSTALL.md
- README.md
