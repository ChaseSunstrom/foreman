# Brainstorm — lens: capability map

Capability-map lens. I compared Foreman with Aider, Cline, OpenHands, SWE-agent, Devin, Cursor, Renovate, Semgrep, CodeRabbit and in-toto/Sigstore. The pack shows heavy depth in proof, guard, queue and calibration. These items are the breadth it doesn't show, best first.

- **Sign proof receipts as in-toto attestations** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: assumption: receipts are Foreman-authored files, and the open questions ask which "proven" labels were later reversed. A signed record of the command, exit code, tree hash and time is checkable by anyone.
  Done when: `fm task prove` emits a signed attestation, and `fm verify <file>` fails after one byte of the receipt or the tree changes.

- **Mark unrunnable checks "unproven" in every receipt** — FIX — value 5 — effort S — risk low — category: proof honesty
  Why: the pack asks how a headless or no-browser UI check avoids reading as a pass. Competing tools usually report skipped checks as green.
  Done when: a UI criterion run with no display yields state `unproven`, and `fm task finish` refuses "proven" on it without a recorded override.

- **Record human overrides as an override ledger** — FEATURE — value 4 — effort S — risk low — category: audit
  Why: the pack asks who records that an override isn't proof. Overrides are hand-set, and no ledger is shown.
  Done when: each override writes who, why and the row it covers, and `fm doctor` lists the overrides still open.

- **Validate "test fails without the change" with mutation testing** — FEATURE — value 4 — effort M — risk med — category: proof strength
  Why: T-2616 and the red-first rule prove a test fails when the fix is removed. Mutation tools (mutmut, Stryker) show whether the test would catch anything else nearby.
  Done when: `fm task prove --mutate` reports the share of mutants the new test kills, and a score below a configured floor warns.

- **Add a PR bot that posts the proof receipt as a comment** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: the demo and README show terminal use only. CodeRabbit and Danger put the evidence where reviewers already look. The push grant already routes through `fm ship`.
  Done when: a PR from a Foreman task carries one comment with the criteria, commands, exit codes and unproven rows.

- **Export the guard as shareable policy packs** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: assumption: guard rules live in the plugin. Semgrep and OPA users expect versioned rule packs with tests and per-project overrides.
  Done when: `fm guard pack install <file>` adds rules, and each rule ships a should-block and a should-allow fixture that the suite runs.

- **Run a restore drill** — FEATURE — value 4 — effort M — risk low — category: ops
  Why: the pack asks what must be rebuilt by hand on a wiped host. The ledgers, bets, timers and steers are all local state.
  Done when: `fm drill restore` rebuilds a scratch home from a backup, runs `fm doctor` against it and lists every missing item.

- **Check ops gauges against an outside signal** — FEATURE — value 4 — effort M — risk low — category: ops
  Why: the pack asks which gauges Foreman trusts only because it wrote them (timer liveness, bet settlement, canary). T-2542 reads systemd, but systemd is the same host.
  Done when: each gauge has a second source (git remote state, CI status, a file mtime on another machine) and `fm doctor` flags disagreement.

- **Quarantine and track flaky tests** — FEATURE — value 3 — effort M — risk low — category: test health
  Why: T-2605 reports a "LeanKind flake" and T-2606 handles a misleading verify command. Mature CI tools track flake rate and rerun policy per test.
  Done when: a test failing then passing on rerun is logged, and a proof run names it flaky instead of failing or passing silently.

- **Export Foreman data as SARIF and OpenTelemetry** — FEATURE — value 3 — effort M — risk low — category: interoperability
  Why: the guard blocks, `fm find` results and hook timings are all Foreman-specific. SARIF feeds GitHub code scanning, and OTel feeds any dashboard.
  Done when: `fm find --sarif` validates against the SARIF schema, and the hook p95 appears in a local OTel collector.

- **Wild: replay a past session against a new model or Foreman version** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild. The long-horizon tier already rolls repos back to old commits. Replaying real recorded sessions would show what a rule or model change would have altered, as record-replay does in browser testing.
  Done when: `fm replay <session>` re-runs the goal in a worktree and prints a diff of verdicts against the original.

- **Wild: let two agents on different models cross-check each other's proof** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: wild. The steers already favour signals Foreman didn't author and cold reads by a different model. Making that a first-class `fm finish --cross` gives each closed task an independent opinion.
  Done when: a finished task records a verdict from a second model that never saw the first agent's reasoning, and a disagreement blocks close.

- **Wild: turn the guard into an on-device "what would have been blocked" dry-run for any shell** — FEATURE — value 3 — effort M — risk med — category: guard reach
  Why: wild. The user hand-types commands to check verdicts, and the pack asks how Foreman could log those without reading shell history. A shell wrapper or `fm guard shell` would explain each command's verdict live and log it for calibration.
  Done when: running `fm guard shell` and entering `rm -rf ~` prints the block and the rule, and the attempt appears in `fm outcomes`.

- **Wild: publish a claims-versus-evidence page that rebuilds itself nightly** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. The user's steers say site claims must match exam lines. Rendering each claim with its source run and an expiry date (red when stale) would be something nobody else ships.
  Done when: the site shows each public number linked to its run id, and a number older than its window turns red.

- **Add cost and token budgets per task, not just per account** — FEATURE — value 3 — effort S — risk low — category: spend
  Why: assumption: `fm budget` caps are global. Aider and Cline users expect a per-task ceiling with an early warning.
  Done when: a task with a cap of N tokens stops and asks at 80%, and the receipt shows spend against the cap.

**Answers to earlier questions through this lens:** a missing ledger class would give wrong answers silently in the calibration readers, since T-2610 counts only finished windows and an absent class reads as "no bets" instead of "unknown". The user hand-checks verdicts with test and guard commands, which `fm guard shell` would capture. Reversed "proven" labels are findable only if past receipts keep the run record, so the attestation item above helps there.

Next question: which capabilities do rival tools ship that users of Foreman are manually approximating with shell scripts today?
Next question: if a stranger installed Foreman today, which single missing integration (CI, PR, editor) would make them leave in the first hour?
