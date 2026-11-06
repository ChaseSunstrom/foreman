---
id: T-1957
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:05:57Z
updated: 2026-10-29T10:13:46Z
batch: [T-1954, T-1955, T-1956]
base: 443d927172f2834200ae41b909836e7de2cda613
base_tree: 6c3fa04fbfc5ae437ca0ef14b72c6d00cd52151a
plan0_at: 2026-10-29T10:06:49Z
plan0_scope: []
verified: strong
---
# fm CLI round 10: task new --json --focus, fm gates ID, finish --numbers
## Raw request
> T-1954: FIX: fm task new --json --focus prints fm focus's text on stdout after the JSON, so piping it into jq fails although the task was made; under --json the focus text goes to stderr
> DONE-WHEN: fm task new --json --focus prints one JSON document on stdout
> T-1955: FEATURE: fm gates takes a task id (fm gates T-1234 uses that task's type and tier), as fm focus's "Done needs: … (fm gates)" line invites; today it is a usage error
> DONE-WHEN: fm gates T-1234 lists that task's gates
> T-1956: FEATURE: fm task finish --numbers "<metric> before → after" fills the Measurements section, so a PERFORMANCE task closes in one call instead of a separate fm task set
> DONE-WHEN: fm task finish --numbers on a PERFORMANCE task passes the numbers gate
## Interpretation
Three small fm CLI gaps hit this session: task new --json --focus breaks jq; fm gates ID is a usage error though fm focus points at fm gates; a PERF close needs a separate fm task set for its numbers.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1954: fm task new --json --focus prints one JSON document on stdout — verify with `python3 plugin/tests/run.py test_cli_ergonomics -k json_focus`
- [x] T-1955: fm gates T-1234 lists that task's gates — verify with `python3 plugin/tests/run.py test_cli_ergonomics -k gates_takes`
- [x] T-1956: fm task finish --numbers on a PERFORMANCE task passes the numbers gate — verify with `python3 plugin/tests/run.py test_cli_ergonomics -k numbers`
## Non-goals
## Approach (options → choice → why)
Focus text to stderr under --json (redirect_stdout); gates type positional drops argparse choices and resolves T-ids via need_brief, else validates the type; finish --numbers sets Measurements with the other sections and _finish_gaps names it. Rejected: JSON-merging the focus output (two documents or a new schema for one flag).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for all three
2. [x] T-1954: task new --json sends fm focus text to stderr
3. [x] T-1955: fm gates resolves a task id
4. [x] T-1956: fm task finish --numbers fills Measurements and the gap check knows it
## Resume here
## Docs impact
MASTER.md done-gates line, CHANGELOG, perf/profiling.md, intake/execute.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli_ergonomics` → ✗ exit 1 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / FAILED (1 classes) [ran] [tree e4f16f1cbb64] (2026-10-29T10:07:25Z)
- `python3 plugin/tests/run.py test_cli_ergonomics` → ✗ exit 1 · Ran 3 tests in 1.8s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e13fd27ddd43] (2026-10-29T10:08:21Z)
- `python3 plugin/tests/run.py test_cli_ergonomics` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:08:21Z)
- (step 2) `python3 plugin/tests/run.py test_cli_ergonomics -k json_focus` → exit 0 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:08:27Z)
- (step 3) `python3 plugin/tests/run.py test_cli_ergonomics -k gates_takes` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:08:29Z)
- (step 4) `python3 plugin/tests/run.py test_cli_ergonomics -k numbers` → exit 0 · Ran 10 tests in 3.6s (8 classes, 16 at a time; slowest: Repeat 3s, Soak 3s, CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:08:33Z)
- (ac 1) `python3 plugin/tests/run.py test_cli_ergonomics -k json_focus` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:13:20Z)
- (ac 2) `python3 plugin/tests/run.py test_cli_ergonomics -k gates_takes` → exit 0 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:13:20Z)
- (ac 3) `python3 plugin/tests/run.py test_cli_ergonomics -k numbers` → exit 0 · Ran 10 tests in 3.5s (8 classes, 16 at a time; slowest: Repeat 3s, Soak 3s, CliErgonomics 1s) / OK [ran] [tree e13fd27ddd43] (2026-10-29T10:13:20Z)
- (audit edge) `self: read the diff; --json focus text goes to stderr and errors still propagate; fm gates ID uses need_brief (names what is here when missing) and keeps a tier override; --numbers is checked with the other gaps before anything runs and written with the other sections` → fm gates BOGUS exits nonzero naming it; lowercase ids are upper-cased by the parser; --numbers 'none: why' passes like --docs [tree e13fd27ddd43] (2026-10-29T10:13:20Z)
- (audit self) `self: read the diff; --json focus text goes to stderr and errors still propagate; fm gates ID uses need_brief (names what is here when missing) and keeps a tier override; --numbers is checked with the other gaps before anything runs and written with the other sections` → no findings [tree e13fd27ddd43] (2026-10-29T10:13:20Z)
## Log
- 2026-10-29T10:05:57Z created
- 2026-10-29T10:06:46Z set tier=S
- 2026-10-29T10:06:46Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_cli_ergonomics -k json_focus`
- 2026-10-29T10:06:47Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_cli_ergonomics -k gates_takes`
- 2026-10-29T10:06:47Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_cli_ergonomics -k numbers`
- 2026-10-29T10:06:49Z focused
- 2026-10-29T10:13:45Z done
- 2026-10-29T10:13:46Z committed 735fb29e (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- playbook CLI errors and argument shape (fm playbooks show fix/cli-errors)
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–5 steps
## Plan gaps
- failed first: step 1 failing tests for all three
## Files touched
- plugin/tests/test_cli_ergonomics.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/skills/intake/references/execute.md
- plugin/skills/playbooks/references/perf/profiling.md
- CHANGELOG.md
