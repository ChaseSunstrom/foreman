---
id: T-2386
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:02:43Z
updated: 2026-10-31T17:46:27Z
builder_model: sonnet
base: f3e0b59618981b3ec016a9c5eff2d360c4d8e274
base_tree: 3cbc3aea25b7e2c33a153bd965dd1bbf02e49511
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:12:41Z
plan0_scope: []
lane_stop: merged 2026-10-31T17:41:38Z
verified: strong
---
# Migration proof for real repos (Mission 7, #6/#10): fm prove --migration runs the repo's own migration tool and the right SQL dialect, and calls a dialect mismatch unproven, not a failure
## Raw request
> Migration proof for real repos (Mission 7, #6/#10): fm prove --migration runs the repo's own migration tool and the right SQL dialect, and calls a dialect mismatch unproven, not a failure
## Interpretation
Reading 1: fm prove --migration runs the repo's own migration tool (dbmate, alembic, Django, prisma) against a throwaway database, in the right dialect, and calls a dialect mismatch unproven. Reading 2: translate Postgres SQL to sqlite and keep sqlite as the only engine. Rejected: a translator is a second source of truth and hides real failures. Today alembic, Django and prisma trees say unknown and a Postgres migration sqlite can't parse reads as a failure.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --migration runs dbmate-format files (one file with -- migrate:up and -- migrate:down sections) and, in a trusted tree whose environment has them, alembic (upgrade head, downgrade base, upgrade head) and Django (migrate, migrate APP zero, migrate) against a throwaway database, comparing the schema after each; prisma and rails trees say what they need instead of unknown — verify with `python3 plugin/tests/run.py test_prove -k migration_tool`
- [x] SQL written for Postgres runs on a throwaway Postgres cluster in a temp dir, unix socket only, when initdb is installed; without it a Postgres-only statement that sqlite rejects makes the verdict unproven (dialect), never fail — verify with `python3 plugin/tests/run.py test_prove -k migration_dialect`
- [x] fm task finish runs fm prove --migration itself when the closing task touched migration files in a trusted tree, and records the run as evidence, so sessions prove migrations by default — verify with `python3 plugin/tests/run.py test_prove -k migration_finish`
- [x] The real database is never reached: DATABASE_URL and the PG and MYSQL connection variables are dropped from the tool's environment, the throwaway database is forced through each tool's own override (alembic's sqlalchemy.url, a generated Django settings module that replaces DATABASES), and a run whose resolved database isn't the throwaway one is refused before any migration runs — verify with `python3 plugin/tests/run.py test_prove -k migration_isolation`
## Non-goals
## Approach (options → choice → why)
1) Extend MIG_TOOLS: the repo's own tool pointed at a throwaway database URL, a temp-dir Postgres (initdb, pg_ctl, unix socket, removed after) when installed, else sqlite with dialect errors classed unproven. Fails if: the tool opens the developer's configured database, which the throwaway URL and T-2288's rule prevent. 2) Use what exists: T-2288's NAME.up.sql/NAME.down.sql runner, sqlite only, as it is. Likely outcome: only repos that write sqlite-portable SQL pairs are covered. 3) Do less: only classify dialect errors as unproven, no new tools or Postgres. Fails if: alembic, Django and prisma trees still say unknown. 4) Run against the developer's configured database. Breaks T-2288's rule: the real database is never opened. Choice 1 (80%): the repo's own tool and a throwaway database are what a real migration needs.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a dbmate file, a stub alembic on PATH, a Postgres-only statement with no initdb
2. [x] MIG_TOOLS entries: the dbmate format, alembic and Django through their own CLI pointed at the throwaway database URL
3. [x] dialect: a temp-dir Postgres (initdb, pg_ctl, unix socket, removed after) when installed, else sqlite with dialect errors classed unproven
4. [x] MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T16:57:02Z step 1/4: failing tests first: a dbmate file, a stub alembic on PATH, a Postgres-only statement with no initdb
- git: worktree-agent-abe8e89db1a0c85e9; 1 uncommitted: plugin/tests/test_prove.py
- touched since last checkpoint: plugin/tests/test_prove.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove -k migration` → ✗ exit 1 · Ran 25 tests in 5.7s (5 classes, 16 at a time; slowest: MigrationFinish 3s, Migration 1s, MigrationTools 1s) / FAILED (4 classes: test_prove.MigrationTools, test_prove.MigrationDialect, test_prove.Mig [ran] [tree 0f9356eaad13] (2026-10-31T16:22:12Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k migration_tool` → exit 0 · Ran 9 tests in 2.3s (1 classes, 16 at a time; slowest: MigrationTools 1s) / OK [ran] [tree 4a45fc50ee1f] (2026-10-31T16:27:40Z)
- (step 3) `python3 plugin/tests/run.py test_prove -k migration_dialect` → exit 0 · Ran 6 tests in 3.0s (1 classes, 16 at a time; slowest: MigrationDialect 2s) / OK [ran] [tree 4a45fc50ee1f] (2026-10-31T16:27:44Z)
- (step 4) `python3 plugin/tests/run.py test_prove -k migration_isolation` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: MigrationIsolation 2s) / OK [ran] [tree 4a45fc50ee1f] (2026-10-31T16:27:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.94s] [ran] [tree 4a45fc50ee1f] (2026-10-31T16:29:15Z)
- (step 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 89 tests in 11.7s (12 classes, 16 at a time; slowest: InfraProof 11s, InfraFinish 9s, DocsProof 9s) / OK [ran] [tree 52bbd97b1413] (2026-10-31T17:02:47Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.77s] [ran] [tree 52bbd97b1413] (2026-10-31T17:03:52Z)
- (step 2) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 89 tests in 6.8s (12 classes, 16 at a time; slowest: InfraProof 7s, InfraFinish 2s, DocsProof 2s) / OK [ran] [tree 8e9566a0b896] (2026-10-31T17:04:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_crash_hygiene test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_edit_cards test_evidence_quality test_extras test_find test_followups test_goal test_graph test_guard test_guard_cases test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_mcp test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_proof test_prove test_reasoning test_recall test_replan test_robustness test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_ship test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_statusline_ui test_steering test_supply_delta test_taste_ledger test_tidy test_tool_proof test_trust test_ui test_ui_signals test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.32s] [ran] [tree 8e9566a0b896] (2026-10-31T17:06:26Z)
- (step 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 89 tests in 7.9s (12 classes, 16 at a time; slowest: InfraProof 7s, InfraFinish 4s, MigrationFinish 4s) / OK [ran] [tree 3c62d6c04196] (2026-10-31T17:42:16Z)
- `python3 plugin/tests/run.py test_prove -k Migration` → ✗ exit 1 · Ran 45 tests in 5.3s (6 classes, 16 at a time; slowest: MigrationFinish 3s, Migration 1s, MigrationDialect 0s) / FAILED (6 classes: test_prove.MigrationDialect, test_prove.MigrationTools, test_prove.M (start tree + this task's tests) [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:06Z)
- `python3 plugin/tests/run.py test_prove -k Migration` → exit 0 · Ran 45 tests in 4.3s (6 classes, 16 at a time; slowest: MigrationFinish 4s, MigrationDialect 2s, Migration 2s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:06Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k migration_tool` → exit 0 · Ran 9 tests in 1.3s (1 classes, 16 at a time; slowest: MigrationTools 1s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k migration_dialect` → exit 0 · Ran 13 tests in 2.6s (1 classes, 16 at a time; slowest: MigrationDialect 2s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (ac 3) `python3 plugin/tests/run.py test_prove -k migration_finish` → exit 0 · Ran 3 tests in 3.4s (1 classes, 16 at a time; slowest: MigrationFinish 3s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (ac 4) `python3 plugin/tests/run.py test_prove -k migration_isolation` → exit 0 · Ran 6 tests in 1.4s (1 classes, 16 at a time; slowest: MigrationIsolation 1s) / OK [ran] [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 5 MEDIUM, 4 LOW fixed red-first in 87a8ac8d before merge; T-2352's gate passed it` → dbmate, alembic and Django through their own CLI on a throwaway; prisma and rails unproven with a need [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 5 MEDIUM, 4 LOW fixed red-first in 87a8ac8d before merge; T-2352's gate passed it` → a driver guard refuses any connect but the throwaway; dangerous Postgres SQL refused; outside script_location refused; trusted trees only via --yes-run [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 5 MEDIUM, 4 LOW fixed red-first in 87a8ac8d before merge; T-2352's gate passed it` → dialect errors judged by text; Debian postgres paths; >1 MB files unproven; version-ordered migrations [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 1 HIGH, 5 MEDIUM, 4 LOW fixed red-first in 87a8ac8d before merge; T-2352's gate passed it` → one tree copy plus ~5 s of Postgres per finish that touches migrations [tree 3612e21a3e3b] (2026-10-31T17:44:24Z)
## Log
- 2026-10-31T14:02:43Z created
- 2026-10-31T16:07:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2386.builder.md
- 2026-10-31T16:07:56Z builder slot freed
- 2026-10-31T16:11:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2386.builder.md
- 2026-10-31T16:11:24Z builder slot freed
- 2026-10-31T16:12:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2386.builder.md
- 2026-10-31T16:12:40Z focused
- 2026-10-31T16:12:41Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:41:38Z merged worktree-agent-abe8e89db1a0c85e9 (7 file(s))
- 2026-10-31T17:41:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abe8e89db1a0c85e9
- 2026-10-31T17:42:07Z focused
- 2026-10-31T17:43:49Z scope: files outside the globs came from merging foreman/build, MASTER (fmmigrate line) and the changelog line
- 2026-10-31T17:44:13Z scope: fmexam.py and fmgenesis.py show in this task's diff because T-2391 merged right after it from the same base; they are T-2391's
- 2026-10-31T17:46:27Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook SQL: query review, indexes and plans (fm playbooks show fix/sql)
- T-2387 [FEATURE M, planned, 4 steps] Data proof (Mission 7, #10): fm prove --data runs a data command on a throwaway copy of its database and checks the task's declared …
- T-2389 [FEATURE M, planned, 4 steps] Release proof (Mission 7, #10): fm prove --release builds the repo's artifact offline, installs it into a throwaway prefix and runs …
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- A check that rereads the config it just wrote proves nothing: guard the connection itself, where every code path has to pass
## Plan gaps
- failed first: step 1 failing tests first: a dbmate file, a stub alembic on PATH, a Postgres-only statement with no initdb
## Files touched
- plugin/tests/test_prove.py
- plugin/lib/fminfra.py
- .fm-scratch/edits1.json
- plugin/lib/fmmigrate.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/tests/test_proof.py
