# Brainstorm — lens: reliability

- **Treat "ran zero tests" as red** — FIX — value 4 — effort S — risk low — category: gates
  Why: assumption: a criterion's verify command like `python3 plugin/tests/test_x.py` can exit 0 after collecting nothing (a renamed module, a wrong filter). T-1205 already hit a verify command naming a module that doesn't exist.
  Done when: a verify command whose runner output says 0 tests ran is recorded as failed, and a test pins that for unittest and pytest output.

- **Bind each proof to the tree it ran on** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: assumption: `fm task prove` and recorded runs are not tied to a tree hash. Closes happen after more edits, especially across forced compactions in long sessions.
  Done when: editing a file after its proof makes `fm task close` print "proof is stale: N files changed since" and refuse, and an untouched tree closes without a re-run.

- **Publish an exit-code and `--json` contract for every verb** — FEATURE — value 4 — effort M — risk low — category: contract
  Why: the unattended drive, `fm run`, `fm ask` and the planned `fm release` branch on verb results. Plain-text parsing is fragile, and the verb count is high (HELP_TIERS conflicts).
  Done when: a table-driven test asserts the documented codes (ok, usage, refused, needs-person) for each verb, and `--json` output matches a golden file.

- **Prove the guard works with state unreadable** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the guard must never weaken. Existing ideas cover a fail-closed canary but not the guard's independence from `.foreman/` state, the disk and the clock.
  Done when: a test runs the 24-dangerous and 25-everyday corpora with the state dir `chmod 000`, HOME read-only and the ledger corrupt, and gets the same 20 stops, 4 saves and 0 false stops.

- **Declare a Claude Code version range per feature** — FEATURE — value 4 — effort M — risk med — category: compatibility
  Why: Foreman was last adapted to 2.1.301 and 2.1.304 is out, with changes that touch it (the skill list re-sent after compaction, `decider: "person"`, the subagent Stop rule). Today drift only shows when something breaks.
  Done when: `fm doctor` lists each hook, mod feature and note as live, degraded or off for the installed version. A feature outside its range turns itself off with a one-line reason, covered by a fake-version test.

- **Run the roundtrip nightly against Claude Code's newest build** — FEATURE — value 4 — effort M — risk low — category: canary
  Why: the e2e roundtrip exists but only runs when someone triggers it. The user wants "latest claude code" and breakage should be found within a day.
  Done when: a scheduled CI job installs the newest published CC, runs `plugin/tests/e2e/roundtrip.py` with Haiku and a dollar cap, and on red opens a captured brief naming the old and new versions.

- **Separate outages from failures in benchmark results** — FIX — value 4 — effort S — risk low — category: benchmarks
  Why: every site claim must be measured, and runs use caps and Haiku. A 529, a rate limit or a cap hit counted as a task fail would skew the Foreman-vs-plain comparison.
  Done when: result files carry `outcome: pass | fail | infra`, infra cases are retried or excluded and listed on the page, and a stubbed 529 test shows no change to pass rates.

- **Run verbs under a hostile environment matrix** — CLEAN — value 3 — effort M — risk low — category: environment
  Why: the macOS job is red (T-1249) and the CI bounds only recently held. Locale, TZ, umask, spaces in HOME, no TTY, `NO_COLOR` and narrow `COLUMNS` are untested axes.
  Done when: one parametrised test runs the core verbs and hooks across at least 6 such environments with identical state results.

- **Expire pending `fm ask` entries tied to dead processes** — FIX — value 3 — effort S — risk low — category: approvals
  Why: approvals are now bound to an exact Claude Code process identity. A process that dies leaves its pending ask unanswerable.
  Done when: killing the asking process makes `fm ask ls` mark the entry expired within one call, and a later `yes` from another process never resolves it.

- **Soak `fm` with parallel processes** — FEATURE — value 3 — effort M — risk low — category: concurrency
  Why: assumption: tests cover single-process state. Parallel builders, lanes and the pane run `fm` at once on about 1,000 briefs.
  Done when: a test runs 8 processes making task and ledger writes for 30 seconds on a scratch repo and ends with `fm doctor` clean, no lost ids and no duplicate ids.

- **Detect a lost foreman-ui patch after a Claude Code update** — FIX — value 3 — effort S — risk low — category: mod
  Why: T-0418 shows the installed mod already lags (0.6.1), and Claude Code updates replace its binary. Assumption: loss is currently silent.
  Done when: `fm doctor` and the first prompt after the CC binary hash changes say the mod is missing or mismatched, with the one fix command, and the pane falls back to plain output.

- **Wild: Show a one-glyph `fm pulse` health light** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: wild. Version skew, hook error counts, guard canary, a stale mod and disk space are scattered across doctor lines. A user glancing at the statusline wants one colour.
  Done when: `fm pulse` prints green, amber or red with the single worst reason, the statusline can show it, and each of the five inputs flips it in a test.

- **Wild: Write a crash capsule on any hook exception** — FEATURE — value 4 — effort M — risk med — category: diagnosis
  Why: wild. Hooks fail open, so crashes pass silently. A sanitised snapshot of the stdin and the touched state, written as a ready-to-run failing test, turns each one into a fix.
  Done when: forcing an exception in a hook produces a `.foreman/crashes/*.py` that fails when run and passes once the bug is fixed, with secrets and absolute paths scrubbed.

- **Wild: Forecast breakage from Claude Code's changelog with `fm doctor --tomorrow`** — FEATURE — value 3 — effort M — risk med — category: compatibility
  Why: wild. The 2.1.304 notes (hook limits, Stop rules, mod `tool.check`) were found by hand. Matching changelog lines against a table of the Foreman surfaces each one touches would flag risk before upgrading.
  Done when: fed the 2.1.302–304 notes, it lists at least the compaction skill-list, `decider` and Stop-subagent items as affecting Foreman, each with its feature name.

- **Wild: Smoke-test the published artifact nightly on a clean HOME** — FEATURE — value 3 — effort M — risk low — category: release
  Why: wild. The user releases often (1.2.36 to 1.2.40 in a short span) and the repo tree can pass while the marketplace or release install path is broken.
  Done when: a nightly job installs the latest GitHub release into an empty HOME, runs `fm doctor` and one Haiku task, and goes red if either fails.
