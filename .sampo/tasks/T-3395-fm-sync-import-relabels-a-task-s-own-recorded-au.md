---
id: T-3395
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T07:11:46Z
updated: 2026-11-06T09:43:38Z
lane: ~/.claude/foreman/.claude/worktrees/agent-adca3e24caa3672f9
lane_branch: worktree-agent-adca3e24caa3672f9
base: 1e1c29e31cc159395ca6ac04cedb714d3fb14c89
base_tree: c52b066e571b19f07ff3d5cc92292ff201c55ec1
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T07:43:04Z
plan0_scope: []
builder_returned: 2026-11-06T08:00:43Z
---
# fm sync import relabels a task's own recorded audits as '(audit X, imported)', and…
## Raw request
> FIX: fm sync import relabels a task's own recorded audits as '(audit X, imported)', and imported audits don't count at close, so with sync on every T-3279 close attempt lost its intent/edge/adversary audits (2026-11-06, two mirror dirs present); an import must never downgrade local audit rows that match the brief's own
## Interpretation
Reading 1: an import must keep audit rows the local brief already has; only mirror-new rows get ', imported'. Reading 2: never mark any audit imported; ruled out, foreign audits must not count here (existing test).
## Assumptions (confidence)
## Acceptance criteria
- [ ] local audit survives export+import and counts at close; foreign audit still imported — verify with `python3 plugin/tests/run.py test_sync -k Audit`
## Non-goals
## Approach (options → choice → why)
1) In _from_mirror, leave audit lines identical to a local line unmarked; fails if export changes the row text. 2) Re-merge local audit rows after import_ writes; likely outcome: a window where rows are marked. 3) Skip import when only audit rows differ; fails when a foreign audit arrives with other edits. 4) use what exists: _from_mirror and c.plain_lines already normalise both sides; likely outcome: works with a few lines. Choice 4 (80%): single choke point, smallest diff, keyed by the full row text incl. timestamp and tree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then fix _from_mirror
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_sync` → ✗ exit 1 · Ran 34 tests in 25.2s (2 jobs, 16 at a time; slowest: Sync 17s, BoardSurfaces 0s) / FAILED (1 classes: test_sync.Sync) [ran] [tree b512cdd9a1b6] [world 2f1906870a] (2026-11-06T07:44:34Z)
- (step 1) `python3 plugin/tests/run.py -k test_sync` → exit 0 · Ran 34 tests in 9.3s (2 jobs, 16 at a time; slowest: Sync 9s, BoardSurfaces 0s) / OK [ran] [tree bdf5dacd9865] [world 2f1906870a] (2026-11-06T07:45:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_sync && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [21.67s] [ran] [tree bdf5dacd9865] [world 2f1906870a] (2026-11-06T07:45:57Z)
- (step 1) `python3 plugin/tests/run.py -k test_sync` → exit 0 · Ran 35 tests in 4.3s (35 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_move_commit_keeps_uncommitted_mirror_edits 0s, Sync.t [ran] [tree 2fd0f6e1e111] [world 2f1906870a] (2026-11-06T08:00:35Z)
## Log
- 2026-11-06T07:11:46Z created
- 2026-11-06T07:42:40Z planned: it has criteria and steps
- 2026-11-06T07:43:03Z focused
- 2026-11-06T07:43:04Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T09:43:38Z criterion 1 verify: `python3 -m unittest plugin/tests/test_sync.py -k Audit` → `python3 plugin/tests/run.py test_sync -k Audit`
- 2026-11-06T09:43:38Z criterion 1 verify moved from a bare 'python3 -m unittest' form (fails from the repo root, where lane merge runs it) to plugin/tests/run.py (T-3411 makes this automatic)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-11-06: Sync is off until T-3342 (.sampo mirror rename) lands: main's old code exports to an untracked .foreman/ while .sampo/ is tracked, and the import si…
