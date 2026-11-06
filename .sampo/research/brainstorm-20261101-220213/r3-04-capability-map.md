# Brainstorm — lens: capability map

- **Track untrusted text into the guard** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: the pack shows injection defenses deferred (T-0791) and search results fenced only as prose. The guard judges the command text alone. Best-in-class tools (CaMeL, Invariant, LlamaFirewall) track provenance. Assumption: fetched and MCP text can be recorded as hashes without a model.
  Done when: a fixture command copied from a fetched page escalates to ask/deny, while the same command typed by the user passes, with no model import in fmguard.

- **Import public injection benchmarks as an exam kind** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the standing rule wants weakness-finding from signals Foreman didn't author. AgentDojo/InjecAgent-shaped cases are external, and the pack shows only child-authored evasions. Assumption: the cases can be vendored as offline fixtures.
  Done when: `fm exam` prints a guard block rate per attack family from at least 20 external-shaped cases, with no network.

- **Lint the permission rules themselves** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the pack covers the guard's code, not the allow/deny rules in settings. The guard has 2 brief-guard false positives, and bypass mode makes an over-broad `Bash(*)` allow costly. Assumption: IAM-Access-Analyzer-style checks (shadowed, overbroad, contradictory rules) are missing.
  Done when: `fm doctor` flags a fixture settings file with `Bash(*)` and a shadowed deny, and passes a tight one.

- **Add a managed-policy layer for headless/server use** — SECURITY — value 4 — effort M — risk med — category: server
  Why: the headless/server column is among the empty cells. A root-owned policy file that user and project settings can only tighten is the standard answer on shared servers. Assumption: nothing like it exists yet.
  Done when: a test shows a project setting that loosens a managed deny is ignored and `fm doctor` names the winning layer.

- **Log writes outside the repo and checkpoint them** — SECURITY — value 4 — effort M — risk med — category: safety net
  Why: bypass mode can edit `~/.bashrc`, `~/.config` or `~/.ssh`, and git checkpoints don't cover those. The pack has door and revert ideas but is repo-centred. Assumption: only fm-visible writes can be caught; a PreToolUse path check is enough for a first cut.
  Done when: a fixture edit to a dotfile is recorded with a pre-image, and `fm undo` restores it byte-for-byte.

- **Export hook and guard events to a local OpenTelemetry collector (opt-in)** — FEATURE — value 3 — effort M — risk low — category: operate
  Why: "operate" for headless/server and Desktop has no pointer to standard observability, and p95 278 ms is only visible through `fm friction`. Off by default, local endpoint only.
  Done when: with the setting on, a collector fixture receives a span per hook run with its latency, and with it off a socket trace shows zero connections.

- **Sign releases with SBOM, hash-chained provenance and an offline vulnerability check** — SECURITY — value 3 — effort M — risk low — category: supply chain
  Why: T-0352 (publish Desktop with CI and release pipelines) is blocked, and ship has only a dependency diff. A SLSA-style attestation lets the "claims manifest" idea be re-verified offline. Assumption: the release path can be run without a network.
  Done when: `fm release verify` on a built artifact checks its SBOM and attestation hash offline and fails when one byte is changed.

- **Add one panic button, `fm halt`** — FEATURE — value 4 — effort S — risk low — category: safety net
  Why: the pack has a night tripwire file, grants and lanes across 8 surfaces, but no single stop. Assumption: users on Desktop, the web UI or MCP can't easily find each switch.
  Done when: one `fm halt` stops lanes, suspends open grants and refuses `fm ship`, and `fm resume` restores them, all shown by a test.

- **Find dead code by sampling line coverage from real sessions** — CLEAN — value 3 — effort M — risk low — category: lean
  Why: "5 of 1219 cards used" shows verb-level data only. Line-level data from sampled hook runs would find branches nobody reaches and pay for the "subtract as you add" rule. Assumption: sampling 1 in N hook runs stays inside the latency budget.
  Done when: a report lists modules with zero executed lines across 500 recorded runs, and the p95 stays within 5% of the baseline.

- **Wild: Make the hooks drop their own privileges with Landlock** — SECURITY — value 3 — effort M — risk med — category: guard (wild)
  Why: assumption: Linux Landlock restricts an unprivileged process without root, so a hook subprocess could only read the repo and the state dir. A compromised or confused hook then can't touch anything else. The cost is a few syscalls on the hot path.
  Done when: a test hook that tries to read `~/.ssh` gets EACCES while normal hooks pass, and p95 grows by less than 5 ms.

- **Wild: Plant a canary token in the injected context to detect leaks** — SECURITY — value 3 — effort S — risk low — category: privacy (wild)
  Why: Foreman injects about 2k chars at SessionStart on every session. A random per-session token there, scanned for in commits, PR text and outbound MCP arguments, shows when injected rules leak. It is the only cheap way to measure that leakage.
  Done when: a fixture commit message containing the token is flagged at `fm task finish`, and a clean one isn't.

- **Wild: Fuzz the guard with a shell-grammar generator, compared against real bash parsing** — SECURITY — value 4 — effort M — risk low — category: guard (wild)
  Why: two brief-guard false positives (a dict key and `.join(` read as paths) show that ad-hoc parsing misses cases. Random valid command strings, compared with `bash -n` and a tokenizer, would find more before users do. Assumption: this goes beyond the child-written evasion idea already listed.
  Done when: a 10k-case run finishes in under 60 s and every disagreement becomes a fixture, with the two known false positives found first.

- **Wild: Meter the cost of Foreman's overhead per reply and show it to the user as a receipt** — FEATURE — value 3 — effort S — risk low — category: lean (wild)
  Why: 387k context per reply is measured, but the user never sees how much of it Foreman added. A one-line "Foreman added N tokens, M ms" at task close turns the lean ratchet from an internal gate into something the user can check.
  Done when: `fm task finish` prints the injected bytes and hook time for the task, and the number matches the `fm cost` breakdown for the same session.

Next question: Which of the 61 empty cells can be answered by pointing at a guard or hook that already exists, and which need a new capability?
Next question: What do the user's own transcripts show about bypass-mode writes outside the repo, and how often?
