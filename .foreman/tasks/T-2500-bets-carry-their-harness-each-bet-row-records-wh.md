---
id: T-2500
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/lib/fmcode.py, plugin/lib/fmexam.py, plugin/lib/fmcli.py, plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-01T19:05:34Z
updated: 2026-11-02T00:54:18Z
rival_at: 2026-11-02T00:35:25Z
rival_split: true
base: 9925ea558d45ec44891e92d02ed2334b30f8ac7d
base_tree: 3e053b4a2e73d1708d5fe00b40d3432182cae8aa
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T00:35:39Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/lib/fmcode.py, plugin/lib/fmexam.py, plugin/lib/fmcli.py, plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md]
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (557) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
verified: strong
---
# Bets carry their harness; fm outcomes --judgment --by-harness splits buckets and Brier by it
## Raw request
> FEATURE: bets carry their harness: each bet row records which harness stated it (claude-code, fm code, codex, gemini, opencode, exam), and fm outcomes --judgment --by harness splits buckets and Brier by it
> DONE-WHEN: a bet from fm code and one from a session land with different harness fields and --by harness shows two rows
## Interpretation
Reading 1: each calibration bet row gets a harness field (claude-code, fm-code, codex, gemini, opencode, exam) read from the process that states it, and fm outcomes --judgment --by-harness prints the buckets and both Briers per harness. Reading 2: the harness is inferred later from the session id's transcript. Reading 1 fits: bet() runs once, in the stating process, and an env marker there is cheap and exact.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bet stated under FOREMAN_HARNESS=fm-code and one under a Claude Code session land with harness fm-code and claude-code; fm outcomes --judgment --by harness --json has a row for each; an old row without the field counts as unknown — verify with `python3 plugin/tests/run.py test_outcomes`
## Non-goals
## Approach (options → choice → why)
1) fmcore.harness(): FOREMAN_HARNESS when set (fm code's child env, the exam's runs, each other agent's hook command exports it), else claude-code when CLAUDECODE or CLAUDE_CODE_SESSION_ID is set, else unknown; bet() stores it; --by-harness groups ledger_data by it (old rows read unknown); fails if: an agent doesn't export the marker (it reads unknown, never a wrong name). 2) use what exists: the session id alone (fm's events tie sessions to agents) ; fails if: fm code and exam runs have no session id. 3) do less: store the field, no --by-harness view; fails if: DONE-WHEN asks for two rows. Choice 1 (75%): one env read at write time, one group-by at read time.
## Risks and rollback
Risk: an agent that never exports the marker reads unknown (a gap, not a wrong label); the other agents' hook commands get the export in the same task only where fmagents writes them. Risk: a forged FOREMAN_HARNESS only mislabels the forger's own bets. Rollback: revert; old rows never had the field and read unknown either way.
Blast radius (fm graph blast): co-changes plugin/lib/fmhooks.py, plugin/lib/fmguard.py, README.md, plugin/tests/test_cli.py, plugin/tests/test_hooks.py; past FIXes T-0875, T-0876, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red test: two focuses with different env write two bet rows with their harness; --by-harness --json groups them; the flag is named in --help
2. [x] fmcore.harness(); fmoutcomes.bet stores it; ledger_data(p, by='harness') groups; fm code's child env and the exam's run env set FOREMAN_HARNESS; the --by-harness flag on fm outcomes; MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_outcomes.CalibrationHarness` → ✗ exit 1 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: CalibrationHarness 1s) / FAILED (1 classes: test_outcomes.CalibrationHarness) [ran] [tree f57387f8723a] [world 2f1906870a] (2026-11-02T00:35:55Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes.CalibrationHarness` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: CalibrationHarness 1s) / OK [ran] [tree 5db4b8d98797] [world 2f1906870a] (2026-11-02T00:37:57Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_code test_judgment test_mcp` → exit 0 · Ran 602 tests in 69.7s (146 classes, 16 at a time; slowest: Worker 69s, Fakes 43s, Survival 21s) / OK [ran] [tree 5db4b8d98797] [world 2f1906870a] (2026-11-02T00:39:07Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 58 tests in 12.8s (16 classes, 16 at a time; slowest: Survival 13s, ModelRouter 8s, CalibrationLedgerBets 8s) / OK [ran] [tree ec348f9d99c8] [world 2f1906870a] (2026-11-02T00:46:24Z)
- (audit intent) `self-review: harness() reads FOREMAN_HARNESS only when it is a short lowercase slug (a forged odd value reads unknown), then FOREMAN_BENCH as exam, then Claude Code's own variables, else unknown; bet() stores it on new rows only; --by harness regroups scored rows with the same tables() and brier(), old rows reading unknown; fm code's env sets fm-code so its bets aren't read as the parent Claude session's` → bets from different harnesses can be compared, and none is labeled with a guess [tree ec348f9d99c8] (2026-11-02T00:46:24Z)
- (audit edge) `self-review: harness() reads FOREMAN_HARNESS only when it is a short lowercase slug (a forged odd value reads unknown), then FOREMAN_BENCH as exam, then Claude Code's own variables, else unknown; bet() stores it on new rows only; --by harness regroups scored rows with the same tables() and brier(), old rows reading unknown; fm code's env sets fm-code so its bets aren't read as the parent Claude session's` → an old row without the field is unknown; 'Bad Name!' in FOREMAN_HARNESS reads unknown; fm code inside a Claude session reads fm-code; a group under 20 scored says too few for a Brier [tree ec348f9d99c8] (2026-11-02T00:46:24Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree ec348f9d99c8] [world 2f1906870a] (2026-11-02T00:48:28Z)
## Log
- 2026-11-01T19:05:34Z created
- 2026-11-02T00:01:56Z planned from capture
- 2026-11-02T00:01:57Z set approved=True
- 2026-11-02T00:35:38Z steer: the flag is --by harness (the request's wording), not --by-harness
- 2026-11-02T00:35:38Z focused
- 2026-11-02T00:35:39Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T00:35:44Z criterion 1 text: a bet stated under FOREMAN_HARNESS=fm-code and one under CLAUDE_CODE_SESSION_ID land with harness fm-code and claude-code; fm outcomes --judgment --by-harness --json has a row for each; an old row without the field counts as unknown → a bet stated under FOREMAN_HARNESS=fm-code and one under a Claude Code session land with harness fm-code and claude-code; fm outcomes --judgment --by harness --json has a row for each; an old row without the field counts as unknown
- 2026-11-02T00:39:09Z scope: fmexam untouched: bench and exam runs already set FOREMAN_BENCH (fmbench._env), which harness() reads as exam
- 2026-11-02T00:47:59Z done
- 2026-11-02T00:48:01Z committed 7210d0c7 (7 files)
- 2026-11-02T00:48:28Z guard authorization added: publish
- 2026-11-02T00:54:18Z publish grant used by fm ship
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: add a `harness` column/field to the bet record (written wherever bets are created, probably in `plugin/lib/fmcore.py` and the `fm bet` / `fm code` paths in `plugin/lib/fmcli.py`), populated from the invoking harness, and add a `--by harness` grouping to `fm outcomes --judgment` so bucket…
- Harness is detected automatically from the environment (e.g. env vars set by Claude Code hooks in `plugin/lib/fmhooks.py`, `fm code` launching a child), versus passed explicitly by the caller as a flag or argument on bet creation. "Session" in DONE-WHEN implies hook-driven detection for claude-code…
- Narrow reading: only the reporting side is new, with harness already partially stored (e.g. in session metadata), and the work is joining bets to their session's harness at query time rather than storing it on the bet row.
- `exam` as a harness value means bets made by eval/exam runs (`plugin/evals/`) are tagged distinctly, so they can be separated from real usage rather than pooled into Brier.
Approaches:
- Store at write time: add `harness` to the bet schema in `fmcore.py`, resolve it through a single `detect_harness()` helper (env var override, then known markers for claude-code/codex/gemini/opencode, `fm code` sets its own value when spawning, exam runner sets `exam`), and have every bet-writing pa…
- Extend `--by` in the `outcomes --judgment` handler in `fmcli.py` to accept `harness` alongside existing keys, reusing the existing bucket and Brier aggregation with the group key swapped, so output is one row per harness.
- Backfill/legacy handling: existing bet rows without the field are grouped under `unknown` at read time rather than rewritten, avoiding a migration of stored data.
- Alternative: derive harness at read time by joining bet → session record. Cheaper to ship but wrong for bets whose session record lacks harness and can't distinguish `fm code` from a claude-code session if both run inside one.
Failure modes:
- `fm code` is itself run from inside a Claude Code session, so env-based detection sees claude-code markers first and tags the `fm code` bet as `claude-code`; DONE-WHEN (two distinct rows) fails unless `fm code` explicitly sets its harness and detection prefers that override.
- Bet rows are parsed strictly elsewhere (`fmcore.py` loaders, `fm replay`, `fm doctor`, `plugin/tests/test_backtest.py` fixtures), so a new field or `unknown` group breaks schema checks or replay determinism.
- `--by harness` output collapses to one row, or Brier is computed over pooled data, if the grouping key is applied only to bucket counts but not to the per-group Brier accumulation in the judgment code.
- Hooks (`fmhooks.py`) run under a latency budget (`bench_hooks.py`) and in a different process than the CLI, so harness detection that shells out or reads session files on every bet regresses the benchmark or returns nothing in the hook path.
## Dissent
- [x] rival reading: Likeliest: add a `harness` column/field to the bet record (written wherever bets are created, probably in `plugin/lib/fmcore.py` and the `fm bet` / `fm code` paths in `plugin/lib/fmcli.py`), populated from the invoking harness, and add a `--by harness` grouping to `fm outcomes --judgment` so bucket… — answered: adopted: a harness field on each bet row, written in fmoutcomes.bet (the one writer), grouped by fm outcomes --judgment --by harness
- [x] rival reading: Harness is detected automatically from the environment (e.g. env vars set by Claude Code hooks in `plugin/lib/fmhooks.py`, `fm code` launching a child), versus passed explicitly by the caller as a flag or argument on bet creation. "Session" in DONE-WHEN implies hook-driven detection for claude-code… — answered: adopted: detected from the environment (FOREMAN_HARNESS, FOREMAN_BENCH, Claude Code's session variables), no flag on the stating verbs
- [x] rival reading: Narrow reading: only the reporting side is new, with harness already partially stored (e.g. in session metadata), and the work is joining bets to their session's harness at query time rather than storing it on the bet row. — answered: rejected: a query-time join needs harness on session records, which fm code and exam runs don't have
- [x] rival reading: `exam` as a harness value means bets made by eval/exam runs (`plugin/evals/`) are tagged distinctly, so they can be separated from real usage rather than pooled into Brier. — answered: adopted: exam = FOREMAN_BENCH runs (fmbench._env sets it), kept apart from real use
- [x] rival approach: Store at write time: add `harness` to the bet schema in `fmcore.py`, resolve it through a single `detect_harness()` helper (env var override, then known markers for claude-code/codex/gemini/opencode, `fm code` sets its own value when spawning, exam runner sets `exam`), and have every bet-writing pa… — answered: adopted in part: one fmcore.harness() helper, fm code sets FOREMAN_HARNESS=fm-code, the exam reads exam; rejected for codex, gemini and opencode: no marker of theirs is known to reach the shell that …
- [x] rival approach: Extend `--by` in the `outcomes --judgment` handler in `fmcli.py` to accept `harness` alongside existing keys, reusing the existing bucket and Brier aggregation with the group key swapped, so output is one row per harness. — answered: adopted: --by harness on fm outcomes (the request's wording), reusing tables() and brier() per group
- [x] rival approach: Backfill/legacy handling: existing bet rows without the field are grouped under `unknown` at read time rather than rewritten, avoiding a migration of stored data. — answered: adopted: old rows without the field read unknown at read time; nothing rewritten
- [x] rival approach: Alternative: derive harness at read time by joining bet → session record. Cheaper to ship but wrong for bets whose session record lacks harness and can't distinguish `fm code` from a claude-code session if both run inside one. — answered: rejected: the same reason as reading 3; and fm code inside a Claude Code session would read claude-code
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2498 [FEATURE M, done, 3 steps] Interim calibration reads and reliability bins: fm outcomes --judgment adds a 7-day… — lesson: When a score needs a month to settle, sh…
- T-2499 [FEATURE M, done, 2 steps] Bets settle with no session: the night tick runs fmoutcomes.maintain; the digest names the kind whose Brier trails its base rate most —…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_code.py, plugin/tests/test_core.py, plugin/tests/test_exam.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-11-01): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/tests/test_outcomes.py; re-ground the plan against them before editing
## Lessons
- Label a record with where it came from at write time, from a marker the writer can't confuse; an unknown is honest, a guessed label poisons every split
## Plan gaps
- failed first: step 1 red test: two focuses with different env write two bet rows with their harness; --by-harness --json…
## Files touched
- plugin/tests/test_outcomes.py
- plugin/lib/fmcore.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- MASTER.md
- CHANGELOG.md
