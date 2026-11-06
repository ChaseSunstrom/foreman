# Brainstorm — lens: simplicity

- **Delete every tunable no run has ever changed** — CLEAN — value 4 — effort M — risk med — category: config
  Why: the 480 s class kill, 15-minute gate wait, 20-minute lease, 10-minute sweep and 300 ms hook budget are each hard-coded with its own rationale. Assumption: most are never set by anyone, so each is a knob with no owner.
  Done when: a grep test finds at most three timing constants outside the deadline module, and the suite passes with the rest folded into it.

- **Ratchet files over 300 lines so they can only shrink** — CLEAN — value 3 — effort M — risk low — category: repo size
  Why: `plugin/lib/` and `plugin/skills/` hold 1,337 files, and the map flags large modules as where dead branches hide. Assumption: long files are where unused paths collect.
  Done when: a gate lists files over 300 lines and fails only when a change adds one or grows an existing one.

- **Cap the journal at ten event types, enforced by a test** — CLEAN — value 3 — effort S — risk low — category: journal schema
  Why: the pane, desk, web UI and mod each parse the journal, so every new event type adds a reader to update. Assumption: the event list has grown one feature at a time.
  Done when: a test fails when the code writes an event name outside the ten listed in one module.

- **Give every verb in `fm help` one example that a test runs** — CLEAN — value 3 — effort S — risk low — category: help text
  Why: the help table is hand-maintained, and the `test_help` collision at position 306 shows it drifts from the commands. Assumption: examples that run stay correct.
  Done when: each verb in `fm help` has one example, and the suite runs each example and checks it exits 0.

- **Invert the guard from a denylist to a twenty-entry allowlist** — SECURITY — value 4 — effort M — risk med — category: command guard
  Why: the guard grows one rule per refused spelling, which is how the fuzz and bypass-report ideas keep arriving. Assumption: a short list of safe command shapes, with everything else refused, is easier to reason about.
  Done when: the allowlist has at most twenty entries, and a 500-command corpus gives the same verdict on every case the current guard refuses.

- **Make every verb read its arguments and nothing else** — CLEAN — value 3 — effort M — risk med — category: CLI surface
  Why: `fm quiet` silently read no stdin, and an inherited 200k window broke ten bench tests (T-1791). Assumption: reading stdin, env and config makes behaviour depend on the caller.
  Done when: any verb run with closed stdin and a poisoned environment prints the same output and exit code as a clean run.

- **Cap the state directory at five top-level files** — CLEAN — value 3 — effort M — risk med — category: state files
  Why: backlog, journal, leases, locks, caches, the memory index and the playbook index are each a separate file with its own write path. Assumption: fewer files mean fewer atomicity bugs.
  Done when: a fixture run leaves no more than five top-level entries in the state directory, and the crash tests still pass.

- **Cut the pane to three panels: work, stage, history** — CLEAN — value 2 — effort S — risk low — category: terminal UI
  Why: the pane shows a work bar, stage rail, steps, Activity lanes, Agents graph, History and Today charts, which the demo has to explain. Assumption: most people look only at the work bar and stage.
  Done when: the pane renders at 80 columns with exactly three panels and the same four keys work.

- **Wild: drop the journal and let `git log` be the audit trail** — CLEAN — value 2 — effort L — risk high — category: audit trail
  Why: wild: every closed task already leaves a commit with a trailer, so the journal duplicates it. Assumption: the commit carries enough to replay a run.
  Done when: a closed task in a fixture repo is reconstructed from `git log` alone, with the same stage list the journal gives.

- **Wild: write settings as one plain sentence in the README** — FEATURE — value 2 — effort S — risk high — category: configuration
  Why: wild: most of the twelve-plus settings are never changed, so "budget $20 a week, never delete" could replace the config file. Assumption: a sentence is enough for the few settings anyone sets.
  Done when: a README line in a fixture parses to the same effective settings as the matching TOML file.

- **Wild: a repo opts out of every hook with one empty file** — FEATURE — value 3 — effort S — risk med — category: opt-out
  Why: wild: the quiet-hours, hands-off and stop-everything ideas each add a separate switch, while one file could disable them all. Assumption: a single kill switch is the simplest way to back out of Foreman in one repo.
  Done when: with `.foreman-off` present in a fixture repo, every hook exits 0 and writes no journal line, and removing the file restores the hooks.
