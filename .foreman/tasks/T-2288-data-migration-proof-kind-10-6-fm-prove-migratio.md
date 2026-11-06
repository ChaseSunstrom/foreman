---
id: T-2288
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T07:06:23Z
updated: 2026-10-31T07:29:55Z
base: 43934c3365b3a325572a9fbd551f44b72811bc9a
base_tree: 57131b67c730e08cb7590c93bef4a4b35ef7ce96
plan0_at: 2026-10-31T07:15:58Z
plan0_scope: []
verified: strong
---
# Data/migration proof kind (#10, #6): fm prove --migration runs a migration up, down and up again on a throwaway database copy and records the schema diff, so a migration task closes on a run, not a claim
## Raw request
> Data/migration proof kind (#10, #6): fm prove --migration runs a migration up, down and up again on a throwaway database copy and records the schema diff, so a migration task closes on a run, not a claim
## Interpretation
Gap map #10/#6: 'data/migration proof (3)'. A migration task closes on the claim that up and down work; nothing runs them. A reversible migration is proven by applying it, reverting it and applying it again on a throwaway database, with the schema compared before and after.
## Assumptions (confidence)
## Acceptance criteria
- [x] for a repo with a recognized migration tool (alembic, django, prisma, plain SQL up/down files), fm prove --migration in a trusted tree runs up, down, up on a throwaway sqlite or a temp schema and records pass/fail with the schema before and after; refuses in an untrusted tree; unknown tools say so — verify with `python3 plugin/tests/run.py test_prove`
## Non-goals
## Approach (options → choice → why)
1) fm prove --migration [PATH]: detect the tool from Foreman's own table (plain SQL up/down pairs first; alembic, django, prisma later as entries), copy the tree to a throwaway dir (as fm prove does), point it at a fresh sqlite file, run up, dump the schema, run down, check it matches the start, run up again and check it matches the first up; trust-gated by fmprove.trusted like any repo-code run; record the result as run evidence on the focused task. 2) parse migrations without running them — rejected: proves nothing about reversibility. 3) run against the project's real database — rejected: never touch real data. Choice 1, starting with plain SQL pairs (fully testable here) and leaving framework entries as data rows to add.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests with a plain SQL up/down fixture
2. [x] the migration runner on a throwaway DB, trust-gated like fm prove
3. [x] docs lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove` → ✗ exit 1 · Ran 12 tests in 1.9s (4 classes, 16 at a time; slowest: VerifyStrength 2s, FindReview 1s, Migration 0s) / FAILED (1 classes) [ran] [tree d5b58adffc63] (2026-10-31T07:16:38Z)
- (ac 1) `python3 plugin/tests/run.py test_prove 2>&1 | tail -25` → ✗ exit 1 · Ran 12 tests in 2.0s (4 classes, 16 at a time; slowest: VerifyStrength 2s, Migration 1s, FindReview 1s) / FAILED (1 classes) [ran] [tree b6c3cab74db3] (2026-10-31T07:17:04Z)
- (step 2) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 12 tests in 2.8s (4 classes, 16 at a time; slowest: VerifyStrength 2s, Migration 2s, FindReview 1s) / OK [ran] [tree 7ab63397637f] (2026-10-31T07:17:26Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_find test_guard_cases test_paused test_prove && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [34.12s] [ran] [tree 7ab63397637f] (2026-10-31T07:18:41Z)
- `cd plugin/tests && python3 -m unittest -q test_prove` → ✗ exit 1 · Ran 7 tests in 0.279s / FAILED (failures=1, errors=6) (start tree + this task's tests) [ran] [tree e1ef079446e8] (2026-10-31T07:28:06Z)
- `cd plugin/tests && python3 -m unittest -q test_prove` → exit 0 · Ran 7 tests in 1.149s / OK [ran] [tree e1ef079446e8] (2026-10-31T07:28:06Z)
- (step 1) `python3 plugin/tests/run.py test_prove test_docs` → exit 0 · Ran 95 tests in 8.3s (26 classes, 16 at a time; slowest: Fences 8s, Migration 1s, FindReview 1s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:28:14Z)
- (step 2) `python3 plugin/tests/run.py test_prove test_docs` → exit 0 · Ran 95 tests in 8.2s (26 classes, 16 at a time; slowest: Fences 8s, Migration 1s, FindReview 1s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:28:23Z)
- (step 3) `python3 plugin/tests/run.py test_prove test_docs` → exit 0 · Ran 95 tests in 8.2s (26 classes, 16 at a time; slowest: Fences 8s, Migration 1s, FindReview 1s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:28:31Z)
- (ac 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 12 tests in 1.4s (4 classes, 16 at a time; slowest: Migration 1s, FindReview 1s, VerifyStrength 1s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:28:33Z)
- (audit intent) `self-review of the diff: trust-gated through fmprove.trusted, a throwaway copy, a fresh sqlite file, an authorizer denying ATTACH, a progress-handler time cap, 500 files of 1 MB at most, cleanup in finally` → Mission 7/#10's data proof: a migration closes on up, down, up run on a throwaway database (test_prove red-to-green) [tree e1ef079446e8] (2026-10-31T07:28:33Z)
- (audit adversary) `self-review of the diff: trust-gated through fmprove.trusted, a throwaway copy, a fresh sqlite file, an authorizer denying ATTACH, a progress-handler time cap, 500 files of 1 MB at most, cleanup in finally` → never the real database; ATTACH denied so a migration can't reach another file; untrusted trees refused [tree e1ef079446e8] (2026-10-31T07:28:33Z)
- (audit edge) `self-review of the diff: trust-gated through fmprove.trusted, a throwaway copy, a fresh sqlite file, an authorizer denying ATTACH, a progress-handler time cap, 500 files of 1 MB at most, cleanup in finally` → a missing down names the migration; a failing down is caught right after it; unknown tools say so [tree e1ef079446e8] (2026-10-31T07:28:33Z)
## Log
- 2026-10-31T07:06:23Z created
- 2026-10-31T07:15:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2288.builder.md
- 2026-10-31T07:15:58Z focused
- 2026-10-31T07:25:20Z merged worktree-agent-af8c98957e6e2ff90 (3 file(s))
- 2026-10-31T07:27:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af8c98957e6e2ff90
- 2026-10-31T07:27:30Z focused
- 2026-10-31T07:28:31Z scope: plugin/lib/fmprove.py (migration, _sql_tool, cmd_migration), plugin/lib/fmcli.py (--migration), plugin/tests/test_prove.py (new), MASTER.md, CHANGELOG.md
- 2026-10-31T07:29:53Z done
- 2026-10-31T07:29:55Z committed 2cbec9f5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2242 [FEATURE M, done, 3 steps] fm prove --bugs: a cheap child reviews the hottest files for bug candidates, each proven by a model-written failing test — lesson: A pr…
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- playbook Schema and data migrations (fm playbooks show fix/migration)
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- similar finished tasks took 2–3 steps
## Lessons
- Prove a reversible change by running both directions on a copy and comparing state, not by reading the files
## Plan gaps
- failed first: step 1 red tests with a plain SQL up/down fixture
## Files touched
- plugin/tests/test_prove.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbudget.py
- plugin/lib/fmexam.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/lib/fmoutcomes.py
- plugin/tests/test_builder.py
- plugin/tests/test_exam.py
- plugin/tests/test_lanes.py
- plugin/tests/test_long.py
- plugin/tests/test_outcomes.py
