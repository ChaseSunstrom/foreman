# Brainstorm — lens: bold bets

- **Squeeze tool output before it enters the context** — PERFORMANCE — value 5 — effort M — risk med — category: cost
  Why: Foreman is about 60% dearer than plain Claude Code in the long session because its context grows faster. T-0828 (compact output) is deferred. Assumption: the foreman-ui mod can rewrite tool results, with oversized output spilled to a file and read back through `fm out N`.
  Done when: the long-session duel on Haiku costs at least 20% less while still passing every hidden test, and a spilled output can be fetched in full.

- **Stub out superseded reads as the session goes** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: Assumption: old file reads and test logs are most of what each compaction has to carry. After a file is edited, its earlier read is dead weight.
  Done when: recorded request bodies show a read replaced by a one-line stub once its file is edited, and the long-session pass rate is unchanged.

- **Add rival plugins as duel opponents** — FEATURE — value 4 — effort M — risk med — category: benchmarks
  Why: The user's first benchmark ask was "against default claude code/other plugins", but the Benchmarks page only shows plain Claude Code. T-0866 and T-0867 are still deferred.
  Done when: `fm bench duel --vs <plugin>` runs the spec suite against an installed rival under the same dollar cap, and the page shows its row.

- **Hold out a private task split from tuning** — FEATURE — value 4 — effort S — risk low — category: benchmarks
  Why: Foreman has been tuned against the public spec suite, so a published win could be overfit. The user's constraint is that every claim be measured.
  Done when: the bench reports tune-split and holdout-split pass rates side by side, and the holdout tasks are never read by any `fm` command that builds a pack.

- **Run an external benchmark subset under Foreman and plain** — FEATURE — value 4 — effort L — risk high — category: benchmarks
  Why: Credibility. Assumption: a Terminal-Bench or SWE-bench-Lite slice can be run on Haiku for a few dollars. Licences and harness fit are unchecked.
  Done when: `fm bench ext --n 10 --cap 5` prints pass rate and cost for both sides.

- **Run Foreman natively on Windows with a PowerShell-aware guard** — FEATURE — value 4 — effort L — risk med — category: platform
  Why: The macOS CI job is red (T-1249), so portability is already shaky. Assumption: Windows is untested and the guard parses only POSIX shells. Many Claude Code users are on PowerShell.
  Done when: a Windows CI job passes the e2e roundtrip, and the safety corpus's PowerShell equivalents are stopped.

- **Cap subagent reports to a short digest** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: The demo leans on scout subagents, whose full reports land in the parent context. Assumption: a SubagentStop hook or the prompt can enforce a limit.
  Done when: the scout's return is at most N tokens in recorded runs, and the fix-the-parser demo still passes.

- **Publish a Known Losses section generated from results** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: The user steered "published whichever way it falls", and site prose figures are still hard-coded (T-1246). Foreman's +10–14% cost and its loss on cost in the long session belong on the page.
  Done when: the page build fails if any result file where Foreman is worse lacks a rendered line.

- **Hunt for losses nightly** — FEATURE — value 4 — effort L — risk med — category: benchmarks — wild
  Why: T-1231 asks Foreman to beat Claude Code, but the suites are hand-written. Assumption: a capped generator over mutated spec tasks will find shapes where Foreman fails or costs more.
  Done when: `fm bench hunt --cap 3` files at least one minimal reproducing brief, or reports "none found" with its seeds.

- **Plant honeytoken credentials that trip an alarm** — SECURITY — value 3 — effort S — risk low — category: guard — wild
  Why: The guard already blocks credential reads. A decoy `~/.aws`-style file that nothing legitimate reads would also show when an injected instruction is probing for credentials, which the guard alone can't reveal (T-0791).
  Done when: reading or exfiltrating the decoy raises a ledger alarm and a pane banner, and a normal session never touches it.

- **Resume from a transcript trimmed between sessions** — PERFORMANCE — value 4 — effort L — risk high — category: long sessions — wild
  Why: Auto-compaction re-sends the skill list and loses detail. Assumption: the session file can be pruned offline of superseded tool results and `claude --resume` accepts it. T-0798 only repairs corrupt transcripts today.
  Done when: a 40k-token session resumes at under half its size, and the quiz of earlier facts is answered as correctly as after a native compaction.

- **Approve dangerous asks with a passkey tap** — SECURITY — value 2 — effort L — risk med — category: approvals — wild
  Why: Self-granted approvals have already been a bug class. Assumption: a local-only WebAuthn check in the web UI is feasible.
  Done when: an ask marked dangerous cannot be granted by any command line or `claude -p` call without a verified assertion from the web UI.

- **Encrypt the ledger and transcripts copied into `.foreman` at rest** — SECURITY — value 2 — effort M — risk med — category: privacy
  Why: Assumption: the ledger and captured briefs hold command lines and user text in plain files, and the Foreman brain may soon travel through git.
  Done when: with the setting on, `grep` for a known secret in `.foreman/` finds nothing, and `fm` verbs still read the data.
