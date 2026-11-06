---
id: T-3190
type: CLEAN
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T10:07:44Z
updated: 2026-11-06T10:03:04Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a50a0db77cf311b6c
lane_branch: worktree-agent-a50a0db77cf311b6c
base: bde7afc07e1a546532ad97af95448441a0b9df0d
base_tree: 2d4ad93f64d5a5c0129271fa648fc6aa01d9471f
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:58:19Z
plan0_scope: []
builder_returned: 2026-11-06T10:03:04Z
---
# Repo DESIGN.md records Sampo's direction (## Point of view, ## Direction with audacity bold), so UI edits stop prompting for one
## Raw request
> No DESIGN.md has a '## Direction' section, so every UI edit prompts for one (T-3170 noticed): write the live page's and the site's direction (modern dashboard by default, forge as a setting; crafted, detailed, animated, never cartoonish) into DESIGN.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] DESIGN.md at the repo root has a concrete ## Point of view and a ## Direction naming audacity bold: modern dashboard with real charts by default, the illustrated forge only as a setting; crafted, detailed, animated, never cartoonish; both themes and phone width — verify with `sampo design sprint .`
- [ ] a UI edit in this repo no longer gets the design-direction note (hooks._design_note finds the direction) — verify with `python3 plugin/tests/run.py test_design`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write DESIGN.md (Point of view, Direction, a pointer to design/sampo/tokens.json for tokens)
2. [ ] verify the sprint's brief and direction stages pass  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `sampo design sprint .` → ✗ exit 1 · · 4 build     the UI files under the root pass fm design lint / · 5 critique  the gates DESIGN.md opts into under ## Gates pass [ran] [tree aedf6cb90901] [world 2f1906870a] (2026-11-06T09:58:35Z)
- (step 1) `python3 plugin/tests/run.py test_design` → exit 0 · Ran 153 tests in 188.9s (33 jobs, 16 at a time; slowest: Rendered 18s, Xray 3s, StaticGates 2s) / OK [ran] [tree aedf6cb90901] [world 2f1906870a] (2026-11-06T10:01:49Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan` → exit 0 · Ran 218 tests in 139.2s (61 jobs, 16 at a time; slowest: RenameScan 7s, ViewsRepair 3s, LockProbe 2s) / OK [ran] [tree aedf6cb90901] [world 2f1906870a] (2026-11-06T10:03:00Z)
## Log
- 2026-11-05T10:07:44Z created
- 2026-11-06T03:11:43Z planned from capture
- 2026-11-06T09:58:18Z focused
- 2026-11-06T09:58:19Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2904 [CLEAN M, dropped, 1 steps] Keep 12's port scripts (port.py, annotate.py) in the repo under site/tools, writing…
- T-3054 [FEATURE L, done, 4 steps] The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting — lesson: A review suggestion t…
- decision 2026-11-03: [cites: user 2026-11-03 'remaking number 2 … more artifact direction'] T-2788 direction: remake direction 2 (Ilmarinen's forge) with the Sampo relic…
- similar past tasks were L: consider --tier L
- similar finished tasks took 4–9 steps
## Behaviour lock
Docs only: DESIGN.md is new; no code changes. test_design still passes.
