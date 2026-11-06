---
id: T-0004
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmdoctor.py, plugin/tests/**]
depends_on: [T-0001]
source: user
created: 2026-09-26T05:02:11Z
updated: 2026-09-26T05:43:04Z
---
# Phase 6: fm tidy and fm doctor
## Raw request
> BUILD_PROMPT.md §3 Phase 6, §9, §12
## Interpretation
fm tidy (§9): dry-run by default, --apply acts, archive before delete, log every change — regenerate STATE/INBOX; archive done/dropped briefs >14d to archive/YYYY-MM; roll ledgers >1 MB into archive/ledger-YYYY-MM.jsonl; list captured items >30d for keep/drop (never delete); auto memory MEMORY.md window/duplicates/dead paths (apply dedupes exact duplicates after archiving a copy); CLAUDE.md + rules lint (budgets, dead paths, stale npm/make commands, duplicates); task graph (cycles, dangling deps, blocked-but-blocker-done); events/hooks.log rotation and old session snapshots; optional --plugins footprint. fm doctor (§12): settings JSON, hook scripts, fixture latency + expected exit codes, hook command collisions on state files, skill-name collisions, always-on budgets, skill/agent frontmatter, briefs parse + STATE matches, MASTER.md file map vs disk, backup present, claude plugin validate --strict (plugin + marketplace), git hygiene (ignored-but-tracked, staged secrets), statusLine wiring, deny rules, rules symlink, scripts parse + setup-plugins --dry-run, --full runs install.sh --no-plugins.
## Assumptions (confidence)
## Acceptance criteria
- [x] tidy dry-run finds seeded rot (dead CLAUDE.md path, duplicate memory lines, 40-day inbox item, dependency cycle); --apply archives without losing anything — verify with `python3 -m unittest test_tidy`
- [x] each doctor check passes on good fixtures and fails on bad ones — verify with `python3 -m unittest test_doctor`
- [x] fm doctor on this machine reports every check; failures are real and explained — verify with `fm doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tidy tests (RED) then fmtidy.py (GREEN)
2. [x] doctor tests (RED) then fmdoctor.py (GREEN)
3. [x] Run fm tidy and fm doctor on the real install; fix what they find
4. [x] Commit phase 6
## Resume here
T-0004 step 1: writing plugin/tests/test_tidy.py (scenario 9 seeded rot; report JSON {applied, projects, findings[{kind,severity,detail,project}]}; kinds: dead_path, stale_command, memory_duplicate, memory_dead_path, inbox_stale, cycle, archive_task, rotate_events, roll_ledger), then implement plugin/lib/fmtidy.py (cmd_tidy; memory dir = ~/.claude/projects/<re.sub('[^A-Za-z0-9]','-',root)>/memory). Next: test_doctor.py + fmdoctor.py. Phases left: T-0005 verification (scenarios, evals, local/verification.md), T-0006 MASTER.md/README/CHANGELOG/uninstall round-trip/final report; disable plugin-dev after Phase 8.
<!-- auto -->
- 2026-09-26T05:36:29Z step 1/4: tidy tests (RED) then fmtidy.py (GREEN)
- git: main; 0 uncommitted
## Verification evidence
- (step 1) `python3 -W error::ResourceWarning -m unittest test_tidy` → 6 tests OK: seeded rot (dead path, stale npm command, duplicate + dead-path memory, 40d inbox, cycle, 20d done task) found in dry run with no changes; apply archives/dedupes with copies, keeps inbox, logs; events rotation; ledger monthly roll; --all (2026-09-26T05:39:05Z)
- (ac 1) `python3 -m unittest test_tidy` → 6 tests OK (2026-09-26T05:39:05Z)
- (step 2) `python3 -W error::ResourceWarning -m unittest test_doctor` → 9 tests OK (each check good/bad fixture + end-to-end --json names all 18 checks) (2026-09-26T05:42:14Z)
- (ac 2) `python3 -m unittest test_doctor` → 9 tests OK (2026-09-26T05:42:14Z)
- (step 3) `fm doctor; fm tidy --all (real install)` → doctor 18 pass / 0 warn / 1 fail (MASTER.md missing: Phase 8 deliverable); tidy found slash-command false positives -> fixed test-first; now 'nothing to do' (2026-09-26T05:43:04Z)
- (ac 3) `fm doctor` → 18/19 pass; the 1 fail (file map: MASTER.md missing) is expected until T-0006 (2026-09-26T05:43:04Z)
- (step 4) `git log --oneline -1` → 5c87b3f feat(hygiene): fm tidy and fm doctor (2026-09-26T05:43:04Z)
## Log
- 2026-09-26T05:02:11Z created
- 2026-09-26T05:02:11Z guard authorization added: core
- 2026-09-26T05:18:58Z set approved=True
- 2026-09-26T05:35:08Z focused
- 2026-09-26T05:43:04Z done
## Follow-ups captured
