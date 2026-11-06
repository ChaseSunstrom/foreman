# Brainstorm — lens: capability map

- **Snapshot the command surface and diff it at close** — FEATURE — value 4 — effort M — risk low — category: contracts
  Why: most recent tasks change `fm` messages, flags and usage lines (`run.py`'s `NAME` usage, docs-impact blockers), and docs-impact only checks that docs exist. A snapshot of subcommands, flags, usage and exit codes would catch unintended surface changes and show which docs to update.
  Done when: removing a flag from a fixture CLI makes `fm task done` list "surface changed: -k removed" and require an acknowledgement or a docs/CHANGELOG touch.

- **Generate changelog and release notes from closed tasks** — FEATURE — value 4 — effort M — risk low — category: release
  Why: the pack mentions "CHANGELOG and MASTER entries" in review notes, which suggests they are written by hand per task. Each closed task already has a title, kind, DONE-WHEN and the commit trailer "(T-2001: T-1998…)".
  Done when: `fm release notes <from>..<to>` prints grouped FIX/FEATURE/PERF entries with task ids, and a test confirms that every closed task in the range appears exactly once.

- **Run a merge train for parallel lanes** — FEATURE — value 5 — effort L — risk med — category: shipping
  Why: recent work includes "never two suites at once", `_theirs` dirty-file attribution and "Ship Tn to main". All of these patch symptoms of several tasks racing toward main. A queue that rebases, tests and fast-forwards one task at a time, with a speculative test of the next, would fix the cause.
  Done when: with two tasks that touch the same file queued, `fm ship` serializes them and the second is rebased and retested before landing. A test asserts that a single test process runs at a time.

- **Declare architecture fitness rules in one file** — FEATURE — value 3 — effort M — risk low — category: invariants
  Why: the open items include splitting `register.tsx` (T-0166) and a "file-ownership invariant test". A rules file could hold "module A must not import B", "file ≤ N lines", and "hook p95 ≤ X ms". These would run as a gate and ratchet over time.
  Done when: adding an import that breaks a rule fails `fm check` and names the rule and the offending line.

- **Install shell completion for subcommands and ids** — FEATURE — value 3 — effort S — risk low — category: DX
  Why: the user types ids and subcommand names constantly ("Ship T-1982", `fm task prove`), and several recent fixes are "name not found" errors. Completion prevents most of them before they happen.
  Done when: `fm completion bash` emits a script, and a test confirms that `fm task d<TAB>` offers `done` and that `T-19<TAB>` lists open task ids.

- **Export OpenTelemetry spans for tasks, gates and hooks** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: gate overlap, hook latency and slow suites are diagnosed by hand, and the pane has no standard export. Spans would let any local Grafana or Jaeger show lane overlap and slow gates. The export would be off by default and local only.
  Done when: with `FM_OTLP=localhost:4318` set, a test collector receives one span per gate with its task id. With the setting unset, no socket opens.

- **Plant canary secrets and assert none leak** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: eval capture, replay pages and the bench corpus all export session data, and T-0035 says "redacted". Redaction has no end-to-end test. Planting fake keys in env, files and transcripts and scanning every export would give it one.
  Done when: a harness runs a fixture session containing canary tokens, then fails if any canary appears in any file produced by the export, capture or replay commands.

- **Hash-chain and sign task receipts** — SECURITY — value 3 — effort M — risk low — category: integrity
  Why: Foreman's claim is that "proof" is commands it actually ran. An agent could edit the ledger. A chained hash per receipt, optionally signed, makes tampering visible to CI or a reviewer.
  Done when: editing one past receipt in the ledger makes `fm doctor` report "chain broken at T-NNNN", and `fm verify <task>` passes on an untouched ledger.

- **Offload chore classification to a local small model** — PERFORMANCE — value 3 — effort M — risk med — category: local-first
  Why: intake tagging, title shaping, capture dedupe and "is this drop noise" (74 of 106 drops) are cheap judgments that currently go to the main model or to hand-tuned heuristics. A local model (assumption: Ollama present) would keep that text on the machine and save tokens. Without a local engine it falls back to today's behaviour.
  Done when: with the setting on and a stub local endpoint, dedupe runs without any outbound call, and a test shows the same result as the heuristic on 20 recorded captures.

- **Show proof coverage as editor gutter marks** — FEATURE — value 3 — effort L — risk med — category: editor
  Why: the surfaces are the terminal, the pane and the web UI, and there is no editor surface. The proving test's coverage data could mark changed lines as "proved" or "unproved" in VS Code or JetBrains.
  Done when: opening a file touched by the focused task shows gutter marks that match `fm task prove`'s coverage output on a fixture.

- **Turn PR review comments into tasks** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: intake already turns pasted text into scoped items with DONE-WHEN. Review comments on a published PR are the next obvious source, carrying a file, a line and a request. Assumption: the user publishes PRs (T-0352 suggests this is coming).
  Done when: `fm intake --pr 12` creates one task per unresolved comment, each scoped to the commented path, and a re-run creates no duplicates.

- **Wild: Run a cross-repo workspace with linked tasks** — FEATURE — value 3 — effort L — risk high — category: workspace
  Why: assumption: the user also maintains Foreman Desktop and the foreman-ui mod (T-0325, T-0418), which are separate trees. A change in the plugin often needs a matching change in the mod and the site. A workspace task would span repos with one DONE-WHEN and one close.
  Done when: one task with two repo scopes cannot close until both repos' gates pass, and `fm status` shows both.

- **Wild: Have a ghost reviewer watch the user's own edits** — FEATURE — value 3 — effort M — risk med — category: pairing
  Why: Foreman guards Claude, but when the user edits by hand (the "protect the user's own edits" idea) nothing checks it. A quiet watcher could run the affected tests and say "this change breaks T-1996's test" after a save.
  Done when: saving a file outside any task triggers a single-line note, with no gate output unless a test fails. Edits outside the project are ignored.

- **Wild: Distribute signed gate packs** — FEATURE — value 2 — effort L — risk high — category: ecosystem
  Why: Foreman has cards (`fm lib show NAME`) and a marketplace plugin format. Gates for Rust, Go or Terraform could be installable packs, each declaring its reads and writes, its network use and its signature. Supply-chain risk is the main cost, so unsigned packs would be refused by default.
  Done when: `fm gate install <pack>` refuses an unsigned or tampered pack, and an installed fixture pack runs as a gate and appears in `fm doctor`.

- **Wild: Run gates under a resource envelope** — PERFORMANCE — value 3 — effort S — risk low — category: scheduling
  Why: the recent overlap fixes show that suites compete with each other and with the user's machine. Running each gate under `nice`/`ionice` or a cgroup, and pausing on battery or high load, would keep the laptop usable. Assumption: Linux (the stated platform) with systemd-run available.
  Done when: a gate launched under load above the configured threshold waits and reports "deferred: load 9.2", and a test confirms that the child process runs with the configured niceness.
