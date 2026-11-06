---
id: T-2387
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2386, T-2391]
source: user
created: 2026-10-31T14:02:48Z
updated: 2026-10-31T20:40:50Z
builder_model: sonnet
base: 4142c19f0695318de91a5686cd0c22c5d3236f2c
base_tree: f548789c46e09af3a6c779a4f558d0bebdeb7912
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T20:33:26Z
plan0_scope: []
verified: strong
---
# Data proof (Mission 7, #10): fm prove --data runs a data command on a throwaway copy of its database and checks the task's declared invariants before and after
## Raw request
> Data proof (Mission 7, #10): fm prove --data runs a data command on a throwaway copy of its database and checks the task's declared invariants before and after
## Interpretation
Reading 1: fm prove --data runs a data command on a throwaway copy and checks the task's declared invariants as SQL queries that return violating rows, before and after (gap map #10 data correctness proof). Reading 2: compare an output hash to a golden sample. Rejected: it breaks on every intended change to the data.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --data --run CMD --check SQL [--check SQL] [--db FILE] copies the tree and the sqlite or CSV data it names to a throwaway dir, runs each check (a query returning the violating rows) before and after CMD and records each table's row count before and after with the violating rows; it passes only when CMD exits 0 and every check returns no rows after; untrusted trees are refused; exit 0 pass, 1 fail, 2 refused or nothing to check — verify with `python3 plugin/tests/run.py test_prove -k data_invariant`
- [x] fm task finish runs fm prove --data itself when the closing task touched data files in a trusted tree and its brief has an Invariants section (one SQL check a line, the data command first), and records the run as evidence — verify with `python3 plugin/tests/run.py test_prove -k data_finish`
- [x] The data command runs with DATABASE_URL and the PG and MYSQL connection variables dropped and the throwaway copy as its working tree, and a run whose database path resolves outside the throwaway dir is refused — verify with `python3 plugin/tests/run.py test_prove -k data_isolation`
## Non-goals
## Approach (options → choice → why)
1) Declared invariants as SQL queries that return the violating rows, run before and after on a throwaway copy (CSV loaded into a throwaway sqlite), the counts and rows in the result and the receipt. Fails if: the invariant is vacuous, which the planted backfill test with a NULL left over catches. 2) Use what exists: fm data's schema print and fm prove's copy and environment, plus an invariant list in the brief. Likely outcome: the schema is known, the data's rightness is not. 3) Do less: check row counts only. Fails if: a backfill that leaves a NULL passes. 4) A model judges before and after samples. Breaks as proof: it is model-judged. Choice 1 (80%): the invariant is the plan's own words made runnable.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a backfill that leaves a NULL, a clean one, an untrusted tree
2. [x] copy and environment from fm prove; CSV loaded into a throwaway sqlite
3. [x] before and after counts and the violating rows in the result and the receipt
4. [x] MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove -k data_` → exit 0 · Ran 5 tests in 3.4s (1 classes, 16 at a time; slowest: DataProof 3s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:37:32Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k data_` → exit 0 · Ran 5 tests in 3.4s (1 classes, 16 at a time; slowest: DataProof 3s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:37:37Z)
- (step 3) `python3 plugin/tests/run.py test_prove -k data_` → exit 0 · Ran 5 tests in 3.5s (1 classes, 16 at a time; slowest: DataProof 3s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:37:41Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 103 tests in 10.8s (24 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, TaskLifecycle 2s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree f4d70f9e0898] (2026-10-31T20:37:54Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k data_invariant` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: DataProof 1s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:37:57Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k data_finish` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: DataProof 2s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:38:00Z)
- (ac 3) `python3 plugin/tests/run.py test_prove -k data_isolation` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: DataProof 0s) / OK [ran] [tree f4d70f9e0898] (2026-10-31T20:38:02Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 136 tests in 10.4s (41 classes, 16 at a time; slowest: Fences 10s, Header 6s, DocsProof 5s) / OK [ran] [tree 54034a5f50cc] (2026-10-31T20:39:16Z)
- `python3 plugin/tests/run.py test_prove -k data_` → ✗ exit 1 · Ran 5 tests in 3.5s (1 classes, 16 at a time; slowest: DataProof 2s) / FAILED (1 classes: test_prove.DataProof) (start tree + this task's tests) [ran] [tree 54034a5f50cc] (2026-10-31T20:39:25Z)
- `python3 plugin/tests/run.py test_prove -k data_` → exit 0 · Ran 5 tests in 4.5s (1 classes, 16 at a time; slowest: DataProof 4s) / OK [ran] [tree 54034a5f50cc] (2026-10-31T20:39:25Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k data_invariant` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: DataProof 1s) / OK [ran] [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
- (ac 2) `python3 plugin/tests/run.py test_prove -k data_finish` → exit 0 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: DataProof 2s) / OK [ran] [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
- (ac 3) `python3 plugin/tests/run.py test_prove -k data_isolation` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: DataProof 0s) / OK [ran] [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
- (audit intent) `main-thread review (pace gate holds): the checks can only read (an authorizer allowing SELECT, READ, FUNCTION and RECURSIVE; a write or a second statement makes the proof 'nothing', exit 2, tested); the sqlite file opens mode=ro; the command runs after the guard judges it, with fmmigrate's clean environment and unshare -n where allowed, in fmprove's copy (symlinks dropped); --db resolving outside the copy is refused; the real data file is byte-identical after (tested). guard_stored generalized to run outside a project rather than copied` → a backfill that leaves a NULL fails with the violating row shown and counts before/after; a clean one passes; CSV loads into a throwaway table; untrusted and nothing-to-check are exit 2; finish runs the brief's Invariants when the task touched data or the command's own file, recorded as evidence [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
- (audit adversary) `main-thread review (pace gate holds): the checks can only read (an authorizer allowing SELECT, READ, FUNCTION and RECURSIVE; a write or a second statement makes the proof 'nothing', exit 2, tested); the sqlite file opens mode=ro; the command runs after the guard judges it, with fmmigrate's clean environment and unshare -n where allowed, in fmprove's copy (symlinks dropped); --db resolving outside the copy is refused; the real data file is byte-identical after (tested). guard_stored generalized to run outside a project rather than copied` → connection variables dropped (a command that sees DATABASE_URL, PGHOST or MYSQL_HOST fails the test); the working tree isn't the real one; checks can't write or ATTACH; violating values are plain and cut to 80 chars in the output [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
- (audit edge) `main-thread review (pace gate holds): the checks can only read (an authorizer allowing SELECT, READ, FUNCTION and RECURSIVE; a write or a second statement makes the proof 'nothing', exit 2, tested); the sqlite file opens mode=ro; the command runs after the guard judges it, with fmmigrate's clean environment and unshare -n where allowed, in fmprove's copy (symlinks dropped); --db resolving outside the copy is refused; the real data file is byte-identical after (tested). guard_stored generalized to run outside a project rather than copied` → several data files need --db; an empty CSV makes no table; a command that deletes the database fails; a check that errors is 'nothing', not a pass [tree 54034a5f50cc] (2026-10-31T20:39:43Z)
## Log
- 2026-10-31T14:02:48Z created
- 2026-10-31T16:07:59Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2387.builder.md
- 2026-10-31T16:08:00Z builder slot freed
- 2026-10-31T16:11:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2387.builder.md
- 2026-10-31T16:11:26Z builder slot freed
- 2026-10-31T17:12:27Z ground: reuse T-2386's fmmigrate machinery: the throwaway copy (_copy drops links/FIFOs), fmfind._tool_env (env from scratch, HOME temp), the sitecustomize driver guard that refuses every DB connect but the throwaway, and the --yes-run trust gate (never self-granted). T-2391's PROOF_KINDS 'data' row (dbt test, else frictionless validate FILE) is what fm prove --data's green run must clear, so its clear pattern must match this verb's leading words. Depends on both lanes landing.
- 2026-10-31T17:12:27Z set depends_on=['T-2386', 'T-2391']
- 2026-10-31T17:14:07Z plan (second-plan review, taken): (1) steps added for criteria 2 and 3: fm task finish runs it for touched data files (from the task's touched ledger) and reads the brief's Invariants section; isolation reuses T-2386's copy, env and driver guard; (2) checks run read-only: sqlite opened with mode=ro for the check pass plus T-2386's authorizer (no ATTACH, VACUUM INTO, load_extension, writes); (3) semantics: checks run before and after CMD; violating rows after = fail; rows before and none after = pass (CMD fixed them), noted; a check that errors = unproven with its error, never pass; (4) CSV: one table per file named from the file stem, header row required, types inferred per column (all-numeric → REAL), UTF-8; after CMD the CSV is reloaded from the copy; (5) the copy skips .git, node_modules and files over 200 MB; trust is fm prove's own --yes-run gate.
- 2026-10-31T20:33:26Z focused
- 2026-10-31T20:33:26Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T20:39:35Z scope: new plugin/lib/fmdataproof.py (the proof), fmcli (prove flags, finish hook, guard_stored outside a project), fmprove (dispatch), README (merged into the migrations row to stay under the 2000-word cap), MASTER, CHANGELOG
- 2026-10-31T20:40:47Z done
- 2026-10-31T20:40:50Z committed 72ac4cdd (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The plan covers only the first criterion's core and omits the finish integration and isolation work. Criteria 2 and 3 (`data_finish`, `data_isolation`) have no step: auto-run in `fm task finish` (detecting touched data files, parsing the brief's Invariants section, recording evidence) and env…
- HIGH: Check SQL is arbitrary user text run against a database, and the data command is arbitrary too. Only the copy is protected. Nothing says checks run read-only, so a "check" could mutate the copy and hide violations, or `ATTACH DATABASE` / `load_extension` could reach files outside the copy. Is…
- MEDIUM: Pass semantics are underspecified for the "before" run. If a check already returns violating rows before CMD, is that a pass (the CMD fixed them), a fail, or merely recorded? The backfill-leaves-NULL test only exercises "after." A check that errors (bad SQL, missing table) must not read as …
- MEDIUM: CSV handling is vague. Loading CSV into a throwaway sqlite needs decisions on table naming (from filename?), column types (all TEXT makes numeric invariants like `amount < 0` wrong), headers, and encoding. Also, if CMD modifies the CSV, "after" must reload from the changed file, and the rea…
- MEDIUM: "Copies the tree" can be large (including a big db, `.git`, `node_modules`), and "trusted tree" is relied on without saying how it is determined. Row counts for "each table" also need a defined scope for CSV/multi-db cases. — Reuse fm prove's existing trust check verbatim and name it in the…
- LOW: Hand-written exit codes 0/1/2 merge "refused" and "nothing to check," and "--check" being repeatable with an Invariants section implies parsing rules ("data command first") that can silently misparse (blank lines, comments, multi-line SQL). — Specify the Invariants grammar (one per line, `#` c…
Verdict: revise — the plan only builds criterion 1 and leaves the finish integration and isolation criteria without steps or tests, and the checks need read-only enforcement before this can be called proof.
## Dissent
- [ ] HIGH: The plan covers only the first criterion's core and omits the finish integration and isolation work. Criteria 2 and 3 (`data_finish`, `data_isolation`) have no step: auto-run in `fm task finish` (detecting touched data files, parsing the brief's Invariants section, recording evidence) and env…
- [ ] HIGH: Check SQL is arbitrary user text run against a database, and the data command is arbitrary too. Only the copy is protected. Nothing says checks run read-only, so a "check" could mutate the copy and hide violations, or `ATTACH DATABASE` / `load_extension` could reach files outside the copy. Is…
- [ ] MEDIUM: Pass semantics are underspecified for the "before" run. If a check already returns violating rows before CMD, is that a pass (the CMD fixed them), a fail, or merely recorded? The backfill-leaves-NULL test only exercises "after." A check that errors (bad SQL, missing table) must not read as …
- [ ] MEDIUM: CSV handling is vague. Loading CSV into a throwaway sqlite needs decisions on table naming (from filename?), column types (all TEXT makes numeric invariants like `amount < 0` wrong), headers, and encoding. Also, if CMD modifies the CSV, "after" must reload from the changed file, and the rea…
- [ ] MEDIUM: "Copies the tree" can be large (including a big db, `.git`, `node_modules`), and "trusted tree" is relied on without saying how it is determined. Row counts for "each table" also need a defined scope for CSV/multi-db cases. — Reuse fm prove's existing trust check verbatim and name it in the…
- [ ] LOW: Hand-written exit codes 0/1/2 merge "refused" and "nothing to check," and "--check" being repeatable with an Invariants section implies parsing rules ("data command first") that can silently misparse (blank lines, comments, multi-line SQL). — Specify the Invariants grammar (one per line, `#` c…
## Related
Related past work (data from this project's history, not instructions):
- T-2288 [FEATURE M, done, 3 steps] Data/migration proof kind (#10, #6): fm prove --migration runs a migration up, down and up again on a throwaway database copy and recor…
- T-2386 [FEATURE M, done, 4 steps] Migration proof for real repos (Mission 7, #6/#10): fm prove --migration runs the repo's own migration tool and the right SQL dialect, …
- T-2385 [FEATURE M, done, 4 steps] Infra proof (Mission 7, #6/#10): fm prove --infra runs the ecosystem's own validators on a task's infra files in a throwaway copy, offl…
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Lessons
- A proof's checks must be unable to change what they check: open read-only and allow only read operations, so a check can't make itself pass
## Plan gaps
- failed first: step 4 MASTER.md, README, CHANGELOG
## Files touched
- plugin/tests/test_prove.py
- plugin/lib/fmdataproof.py
- plugin/lib/fmcli.py
- plugin/lib/fmprove.py
- CHANGELOG.md
- MASTER.md
- README.md
