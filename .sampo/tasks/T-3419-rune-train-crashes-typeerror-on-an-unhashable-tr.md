---
id: T-3419
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:57:37Z
updated: 2026-11-06T10:03:17Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ac220293cfd9ccf1c
lane_branch: worktree-agent-ac220293cfd9ccf1c
base: bde7afc07e1a546532ad97af95448441a0b9df0d
base_tree: 2d4ad93f64d5a5c0129271fa648fc6aa01d9471f
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:58:11Z
plan0_scope: []
builder_returned: 2026-11-06T10:03:17Z
---
# rune._train crashes (TypeError) on an unhashable train id in a tower's exam.jsonl;…
## Raw request
> FIX: rune._train crashes (TypeError) on an unhashable train id in a tower's exam.jsonl; T-3376 only contains it per tower in kalevala watch, so make _train skip or stringify a bad id and log it
## Interpretation
_train skips non-scalar train ids, stringifies scalars, logs one note per call.
## Assumptions (confidence)
## Acceptance criteria
- [ ] _train survives a list/dict id among good rows — verify with `python3 plugin/tests/run.py test_genesis.GenesisRead.test_train_skips_unhashable_ids`
## Non-goals
kalevala watch containment (T-3376).
## Approach (options → choice → why)
Guard inside _train (the single caller path); one hooks.log_error per call.
## Risks and rollback
## Execution prompt
## Steps
1. [x] guard _train, test with a bad row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → exit 0 · Ran 29 tests in 56.4s (2 jobs, 16 at a time; slowest: GenesisRead 9s, GenesisReadRecord 1s) / OK [ran] [tree 18d1f45d9b77] [world 2f1906870a] (2026-11-06T09:59:18Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_genesis test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.78s] [ran] [tree 18d1f45d9b77] [world 2f1906870a] (2026-11-06T10:02:05Z)
## Log
- 2026-11-06T09:57:37Z created
- 2026-11-06T09:57:53Z set tier=S
- 2026-11-06T09:58:09Z planned: it has criteria and steps
- 2026-11-06T09:58:10Z focused
- 2026-11-06T09:58:11Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3376 [FIX M, active, 1 steps] Kalevala watch(): one unreadable tower file blanks the whole Kalevala block instead of…
- T-3333 [FEATURE M, planned, 3 steps] Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts me…
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- similar past tasks were M: consider --tier M
