# Brainstorm — lens: bold bets

- **Replay the user's own history through Foreman at install** — FEATURE — value 5 — effort M — risk low — category: first-run value
  Why: evidence A shows a new user gets abstract prose and no proof of value. Claude Code transcripts already sit on the machine. Replaying the last ~10 sessions through the guard and done-gate, locally with no model calls, would list "3 things Foreman would have stopped in your own work". The existing guard-replay corpus work is aimed at developing Foreman, not at onboarding.
  Done when: on a HOME with 5+ transcripts, `fm tour --history` prints at least one real past command or "done" claim that would have been blocked or flagged, with its transcript line, and makes zero network calls.

- **Measure Foreman's lift from the user's own pre- and post-install transcripts** — FEATURE — value 5 — effort M — risk med — category: proof of value
  Why: evidence C: the bench has 1 case and 3 court cases at 0/3, so there is "no published evidence Foreman helps". Transcripts from before install give a free baseline: corrections per session, rework, tokens per finished task. Install should snapshot that baseline.
  Done when: `fm lift` prints before/after medians for at least 3 metrics with sample sizes, and says "insufficient data" under a stated minimum.

- **Make install plan-then-apply, with bypass earned instead of defaulted** — SECURITY — value 5 — effort M — risk med — category: trust
  Why: evidence A2: a default install sets bypassPermissions, installs third-party plugins, adds 20 deny rules and a statusline wrapper, and only says "Claude Code asks you to confirm once". Proposal: print a numbered change list first (`--yes` skips it). Third-party plugins and bypass become separate opt-ins. `fm doctor` offers bypass later, citing guard-corpus results. Assumption: the guard still holds without bypass.
  Done when: running `install.sh` in a clean HOME with no flags and no `--yes` changes nothing until confirmation. The default result has defaultMode unchanged and no third-party plugins. `--yes --bypass` reproduces today's setup.

- **Ship `fm demo`, a 60-second scripted run with no model calls** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: evidence A1 (no demo or before/after) and A11 (jargon). A cassette-driven session in a temp repo (a seeded bug, FIX → plan → red → green → evidence → done) shows each term at the moment it matters. Assumption: the fake-model cassette harness already exists for tests and can be reused.
  Done when: `fm demo` finishes in under 90 seconds in a clean HOME, touches nothing outside its temp directory, and prints the finished task with its evidence.

- **Put `fm` on the shell PATH at install** — FIX — value 5 — effort S — risk low — category: install
  Why: evidence A3: README says "run fm …" everywhere, but a shell gives "command not found".
  Done when: in a fresh login shell after install, `command -v fm` resolves. Uninstall removes the shim and leaves no residue.

- **Stop a fresh install from failing its own `fm doctor`** — FIX — value 4 — effort S — risk low — category: first-run
  Why: evidence A8: a fresh install fails on "missing backup" and prints 40 lines of passes. Give "not yet run" its own state, and print one line when everything is green.
  Done when: `fm doctor` right after a clean install exits 0 with at most 3 lines of output.

- **Make `fm repeats` suggest only whole-suite gates** — FIX — value 3 — effort S — risk low — category: gates
  Why: evidence C: it suggests single test modules as every-task gates, which is bad advice. A single module would also be a weak gate.
  Done when: with a command history that includes `python3 -m unittest test_x`, `fm repeats` proposes only the full-suite command, and a test pins that.

- **Give folded tasks their parent's grade in `fm digest`** — FIX — value 3 — effort S — risk low — category: observability
  Why: evidence C: 159 of 370 tasks in the last week show as "ungraded", so the headline numbers hide 43% of the work.
  Done when: digest ungraded count falls to the tasks with no parent, and a folded task shows `via T-nnnn`.

- **Stop `capture` then `task new` from duplicating, and list valid values in `task new --help`** — FIX — value 3 — effort S — risk low — category: CLI
  Why: evidence A6: `fm task new` without `--from` duplicates the capture, and `--help` names no `--type` or `--tier` values and gives no example.
  Done when: `task new "same text"` after a capture offers to adopt the capture (or does so), and `--help` lists the types and tiers with one example.

- **Replace the seven `_git` copies with one module** — CLEAN — value 3 — effort M — risk low — category: maintainability
  Why: evidence D lists seven copies of `_git` in lib. One module with one timeout and error policy cuts the drift risk without changing behaviour.
  Done when: `grep -rn "def _git" plugin/lib` finds one definition, and the suite plus `fm doctor` still pass.

- **Wild: Publish a live "held rate" badge computed from the ledger** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: evidence C: 670 of 688 tasks held, 18 fixed later (2.6%). A badge linking to the 18 reopened tasks makes the claim checkable and keeps it honest. It must be opt-in for private repos (sensitive-repo rule).
  Done when: `fm badge` writes a static SVG and a linked list of reopened tasks, and refuses in a sensitive repo unless `--force` is passed.

- **Wild: Print an install "nutrition label"** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: evidence A2 and C: users cannot see what Foreman costs them. The label would show always-loaded words (~1k rules), SessionStart size (~1.5k chars), hook p95 ms, deny rules added and background processes. It is generated from measurements, not prose.
  Done when: `fm label` prints those five numbers, each tagged with how it was measured, and the README quotes the same output.

- **Wild: Detect first-week confusion and file it as a task against Foreman** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: evidence A shows every newcomer problem was found by an outside probe. Locally counting "command not found", `--help` calls, refusals hit twice and `fm init` without a following task would let Foreman find the next A-list itself. Data stays on the machine, and a task is filed only with consent. Assumption: the existing hook ledger records command failures.
  Done when: replaying a scripted newcomer log yields at least 3 friction tasks, each citing the logged event, and none are filed without a yes.
