---
id: T-3333
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/sync.py, plugin/tests/test_kalevala.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:32:03Z
updated: 2026-11-06T07:01:19Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a6594317511297181
lane_branch: worktree-agent-a6594317511297181
base: 529a3fe0fde3b8d2a3695a2bbec5a028991cff17
base_tree: e9852af9e333832b952bca409fda465999846644
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:28:11Z
plan0_scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/sync.py, plugin/tests/test_kalevala.py]
builder_returned: 2026-11-06T07:01:19Z
---
# Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts merge by line, generation numbers come from a claim
## Raw request
> Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts merge by line, generation numbers come from a claim
## Interpretation
Reading 1: gate Kalevala towers by tower:<name> claims and line-merge exam/acts. Reading 2 (ruled out): a new fleet scheduler; too big, claims already exist.
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones stepping one project against a bare remote run each tower once per round and log each act once; a vanished machine's towers are taken over after its lease lapses; exam.jsonl and the acts log travel and merge by line; keep/revert is computed identically on both from the merged scores — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
1) claims API gate in step/_decide, line-merge in sync: likely outcome each tower runs once per round; fails if remote is down. 2) lock files in the mirror: fails under concurrent push, racy. 3) use what exists: T-3321 claims.py take/list is what option 1 calls, likely outcome the smallest diff. 4) do less: only merge exam and acts, skip steers: likely outcome steers diverge. Choice 1 (80%): reuses T-3321.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py, plugin/lib/fmkalevala.py, plugin/lib/sampo/moonscale.py, MASTER.md.
## Execution prompt
## Steps
1. [ ] two-clone test, red  <- CURRENT
2. [x] tower claims in step and _decide
3. [x] line-merge travel for exam.jsonl, acts, steers.md
## Resume here
<!-- auto -->
- 2026-11-06T06:55:08Z step 1/3: two-clone test, red
- git: worktree-agent-a6594317511297181; 2 uncommitted: plugin/lib/sampo/sync.py, plugin/tests/test_kalevala_fleet.py
- touched since last checkpoint: plugin/tests/test_kalevala_fleet.py, plugin/lib/sampo/sync.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala_fleet` → ✗ exit 1 · Ran 5 tests in 79.3s (1 jobs, 16 at a time; slowest: KalevalaFleet 1s) / FAILED (1 classes: test_kalevala_fleet.KalevalaFleet) (ran] (tree c8d9e872690f] (world 2f1906870a] (2026-11-06T06:31:34Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala_fleet` → exit 0 · Ran 5 tests in 33.1s (1 jobs, 16 at a time; slowest: KalevalaFleet 1s) / OK (ran] (tree 3bd9b9d829d7] (world 2f1906870a] (2026-11-06T06:35:33Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala test_sync` → exit 0 · Ran 95 tests in 119.9s (12 jobs, 16 at a time; slowest: KalevalaStep 13s, Sync 8s, KalevalaWatch 4s) / OK (ran] (tree 3bd9b9d829d7] (world 2f1906870a] (2026-11-06T06:37:34Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_kalevala test_kalevala_fleet test_left_out test_models test_rename_scan test_sync && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 311 tests in 586.5s (91 jobs, 16 at a time; slowest: KalevalaStep 20s, RenameScan 8s, Bench 6s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 3bd9b9d829d7] (world 2f1906870a] (2026-11-06T06:47:35Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala_fleet test_kalevala test_sync` → ✗ exit 1 · Ran 98 tests in 27.4s (30 jobs, 16 at a time; slowest: KalevalaStep 10s, KalevalaFleet 6s, KalevalaWatch 2s) / FAILED (1 classes: test_sync.Sync.test_the_mirror_does_not_change_the_worktree_id) (ran] (tree 57d8323a3cc5] (world 2f1906870a] (2026-11-06T06:58:53Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala_fleet test_kalevala test_sync` → exit 0 · Ran 98 tests in 17.7s (12 jobs, 16 at a time; slowest: KalevalaStep 11s, Sync 7s, KalevalaFleet 6s) / OK (ran] (tree 5504f914595e] (world 2f1906870a] (2026-11-06T06:59:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_kalevala test_kalevala_fleet test_left_out test_models test_rename_scan test_sync test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 459 tests in 85.6s (130 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaFleet 5s, ConfidenceRoutes 4s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 5504f914595e] (world 2f1906870a] (2026-11-06T07:01:02Z)
## Log
- 2026-11-06T04:32:03Z created
- 2026-11-06T06:28:08Z focused
- 2026-11-06T06:28:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:54:14Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3321 [FEATURE M, active, 3 steps] Fleet part 1: claims on git refs: take, renew, release and list claims under refs/sampo/<slug>/claim/<key> by atomic compare-and-swap…
- T-3266 [FEATURE M, active, 3 steps] Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_moons_scale] Every feature the user asks for that a generator never proposed is traced to the prompt line o…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_kalevala.py, plugin/tests/test_sync.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/kalevala.py, plugin/lib/sampo/sync.py; re-ground the plan against them before editing
