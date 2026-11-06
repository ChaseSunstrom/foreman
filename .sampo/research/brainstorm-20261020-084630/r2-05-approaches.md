# Brainstorm — lens: approaches

- **Add rival plugins as duel contestants** — FEATURE — value 4 — effort M — risk med — category: benchmarks
  Why: your original ask was benchmarks "against default claude code/other plugins", but the published duels are Foreman vs plain Claude Code only. Assumption: one or two popular discipline plugins can be installed headlessly in a throwaway HOME. Trade-off: it costs more per run, so use Haiku with dollar caps, and each rival's install steps must be fair and published.
  Done when: `fm bench duel --vs <plugin>` runs the spec suite for it under a dollar cap, and the Benchmarks page shows its pass, cost and time rows next to Foreman's.

- **Benchmark the false-done rate on impossible tasks** — FEATURE — value 4 — effort M — risk low — category: benchmarks
  Why: the pitch is "prove its work", yet on small specified tasks both sides pass everything, so the duel can't show it. Seed tasks that cannot be finished (a contradictory spec, a test that can't go green, a missing dependency) and score only whether the final message claims success. Assumption: plain Claude Code claims done on a real share of these.
  Done when: a spec-suite subset with unfinishable cases reports a "claimed done wrongly" count per side, from 3 runs, on the Benchmarks page.

- **Budget `fm` calls and stdout per closed task** — PERFORMANCE — value 4 — effort S — risk low — category: cost
  Why: the long session costs ~60% more ($0.095 vs $0.059) because bookkeeping calls and notes grow the context, and T-1231 is still deferred. Bytes per hook are covered elsewhere; this counts the `fm` verbs' own tool calls and result size, then shrinks the top offenders with a `--full` opt-in.
  Done when: a test over a recorded session prints calls and stdout bytes per verb, and a CI ratchet fails if the median per closed task grows.

- **Mirror the hardest guard rules into native permission deny rules** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard is a hook, so it protects only while the hook runs and Foreman is installed. Generating `permissions.deny` entries from the credential-read, exfiltration and system-chmod corpus gives a second layer in the same bypass mode. Assumption: deny rules still apply in bypass mode on 2.1.304. Trade-off: native patterns are coarser, so mirror only the rules that map cleanly.
  Done when: with the guard hook disabled, a headless run of each mirrored dangerous command is still refused, and the 25 everyday commands are not.

- **Ship an observer mode with zero injected context** — FEATURE — value 4 — effort M — risk low — category: adoption
  Why: Foreman's cost comes from injected notes and bookkeeping, and some users won't accept that. Observer mode adds no skills and no notes. It reads the transcript afterwards with deterministic checks (edits with no test run, "done" with no proof, risky commands) and prints a report.
  Done when: `fm observe <session>` lists violations with turn numbers and makes no model call, and an installed observer adds 0 bytes to the context in the bench.

- **Benchmark prompt injection planted in the repo** — SECURITY — value 4 — effort M — risk low — category: benchmarks
  Why: safety is your strongest measured result (20 of 24 dangerous commands stopped), but it covers only commands typed at the model. T-0791 is deferred. Plant instructions in a README, a code comment and a tool output, then score whether the agent runs the exfil or credential command.
  Done when: the suite has at least 6 planted-instruction cases and publishes an executed-vs-stopped count per side.

- **Test a terse output style for output-token savings** — PERFORMANCE — value 3 — effort S — risk med — category: cost
  Why: output tokens are the priciest per token, and nothing in the pack touches narration length. Ship an optional output style and run the duel with and without it. Trade-off: it may hurt pass rate, so it ships only if the duel shows a win.
  Done when: a duel run reports output tokens and pass rate for the style on and off, and the page keeps the style only if the pass rate holds.

- **Let a prompt prefix drop ceremony for one request** — FEATURE — value 3 — effort S — risk low — category: user control
  Why: the cost complaints are about small asks paying for plan, proof and bookkeeping. A per-request escape (the guard stays on) is cheaper than a global mode switch. Assumption: users want this per request, not per session.
  Done when: a prompt starting with the prefix creates no task and injects no plan note, and the guard still refuses a dangerous command in that turn.

- **Wild: Launch through `fm claude`, which picks hooks and compaction window per repo** — FEATURE — value 3 — effort M — risk med — category: launcher
  Why: 2.1.304 allows `k`/`M` suffixes on the compaction window, and the skill listing is re-paid after every compaction. A launcher could pass a `--settings` overlay and env chosen from the repo map and queue shape, so a one-file repo doesn't carry a marathon's configuration. Assumption: the CLI's settings overlay flag is stable.
  Done when: `fm claude` in a tiny repo starts a session with a smaller listing and hook set than in this repo, and `fm doctor` shows which profile it chose.

- **Wild: Publish a generated Losses page** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: every claim on the site must be measured, and the 60% long-session cost is already disclosed. A page generated from the results files, listing every case Foreman lost or cost more on, makes the wins credible. It also removes hard-coded prose (T-1246).
  Done when: the build regenerates the page from the results JSON, and adding a losing result file adds a row with no hand edit.

- **Wild: Stamp commits with proof and cost trailers** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: `git log` becomes a dataset of what each change cost and which command proved it, with no extra store. Assumption: per-task cost is already in the ledger. Trade-off: trailers are public if the repo is, so cost figures need an opt-in.
  Done when: a closed task's commit carries `Foreman-Proof:` and `Foreman-Cost:` lines, and `git log --format=%(trailers)` lists them.

- **Pair idle compaction with queue waits** — FEATURE — value 2 — effort S — risk low — category: cost
  Why: 2.1.304 adds an Idle compaction setting. When the queue is waiting on the user, compacting while idle means the next prompt starts on a small context. Assumption: it only pays when the idle gap exceeds the prompt-cache window.
  Done when: `fm doctor` reports the idle-compaction setting and warns when an unattended-drive config would leave it off.
