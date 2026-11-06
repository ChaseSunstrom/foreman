# T-0024 / T-0025 grounding (2026-09-26)

## Today
- `fm task evidence ID [--step N|--ac N] CMD RESULT` (fmcli.py ~185, parser ~710): both strings typed by Claude;
  Brief.add_evidence (fmcore ~653) redacts, flattens and appends "- (step N) `cmd` → result (ts)".
- Nothing runs the command, so a typo ("272 tests" for 267) or a masked failure (`unittest | tail -1 && commit`) is
  recorded as fact. `fm task step ID done N` only checks that evidence exists.

## Design
- T-0024: `fm task evidence ID --step N --run "<cmd>" [--timeout S]`: bash -c the command in the project root,
  record "exit N · <last non-empty output line(s), ≤200 chars>" as the result (RESULT positional becomes optional
  with --run), print the tail, exit with the command's code. A failed run is recorded with a ✗ marker;
  `fm task step done` / `ac check` refuse while the newest evidence for that step/criterion is a ✗ run.
- T-0025: `fm check [add "<cmd>" | rm N | list]` stores the project's gate commands in meta (via fm), and `fm check`
  runs them all (same runner as --run), prints ✓/✗ per command with exit codes, exits 1 on any failure;
  `--evidence ID --step N` records one evidence line per gate.
- Guard (core change): commands run by fm are invisible to the Bash guard. The fm branch of check_bash must run
  check_bash (depth+1) on `--run` values and on `fm check add` values, so fm can't launder a blocked command.
  Stored checks only enter through the guarded `add`.
