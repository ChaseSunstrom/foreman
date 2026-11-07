---
id: T-3506
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:06:01Z
updated: 2026-11-06T19:11:57Z
lane: ~/.claude/foreman.lanes/T-3506
lane_branch: foreman/T-3506
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:08:56Z
plan0_scope: []
---
# setup links ~/.local/bin/sampo beside fm, doctor checks it, and install rewrites an outdated Foreman block in ~/.claude/CLAUDE.md
## Raw request
> setup links ~/.local/bin/sampo beside fm, doctor checks it, and install rewrites an outdated Foreman block in ~/.claude/CLAUDE.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] setup links sampo and fm, sampo doctor names a missing sampo link, and install-user replaces a CLAUDE.md block that differs from the current one (the old '# Foreman' block included) — verify with `python3 plugin/tests/run.py test_setup`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] link sampo, doctor check and block rewrite, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_setup test_doctor` → exit 0 · Ran 168 tests in 16.8s (54 jobs, 16 at a time; slowest: ViewsRepair 6s, LockProbe 3s, Command 3s) / OK [ran] [tree 3b4b667c0972] [world 2f1906870a] (2026-11-06T19:11:57Z)
## Log
- 2026-11-06T19:06:01Z created
- 2026-11-06T19:06:18Z lane: ~/.claude/foreman.lanes/T-3506 on foreman/T-3506
- 2026-11-06T19:08:56Z focused
- 2026-11-06T19:08:56Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T19:11:00Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1324 [FIX S, done, 2 steps] fm doctor notices a missing or wrong ~/.local/bin/fm link and says the fix — lesson: Every install step that matters outside Claude Code (a…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- research readme-site-audit: Seven read-only auditors, one per slice; each claim checked against code and live data. Findings below are verified
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- similar finished tasks took 2–9 steps
