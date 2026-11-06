# Brainstorm — lens: simplicity

- **Derive "self" from the repo's own scripts** — SECURITY — value 5 — effort S — risk med — category: guard
  Why: Thymic AIRE shows the body every tissue antigen before it judges. Frontier: 15+ approval prompts per session. Prior art: prefix allow lists (Claude Code, Codex). Better by: self comes from Makefile, package.json scripts and CI steps, so prompts fall without a hand-written list. Novelty 3.
  Done when: running each declared repo script triggers no prompt or nudge, and the 124-case replay corpus gives the same verdicts.

- **Contract after an incident** — CLEAN — value 4 — effort M — risk low — category: learners
  Why: After an infection, about 90% of effector cells die and a few memory cells stay. Foreman's incident artifacts (hints, temporary rules, fever caution, lessons) have no end. Prior art: none found in harnesses. Better by: a closed FIX leaves one lesson line and an auto-retire check, and the rest is deleted. Novelty 4.
  Done when: closing a FIX task drops its injected chars to at most one lesson line, and the retired items are listed in one receipt.

- **Compete for fixed niche slots** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: Lymphocytes survive only by winning scarce survival signals, so the repertoire size stays constant. Evidence: 1214 unused stack cards and 28 deferred bundles. Prior art: LRU caches, none for agent memory. Better by: one cap across lessons, learned rules, triggers and cards, where a recall or fire renews the slot. Novelty 3.
  Done when: adding the (N+1)th learned artifact evicts the least-renewed one, and a test shows an artifact that was recalled survives.

- **Write every incident as one line** — CLEAN — value 4 — effort S — risk low — category: schema
  Why: Antibodies are one structure with variable ends. Foreman keeps lessons, guard cases, triggers and bets in different shapes. Prior art: none found. Better by: one row of signature, response, expiry and replay case feeds all four. Novelty 3.
  Done when: a lesson, a guard rule and a trigger are all created from that row format, and `fm replay` reads the row's own case.

- **Index guard rules by command head** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: Lymphocytes home to tissues instead of checking every cell. Evidence: hook p95 is already a lean-ratchet metric. Prior art: ordered rule lists. Better by: the hot path checks at most 3 rules per call. Novelty 2.
  Done when: p95 on the replay corpus drops, and all 124 verdicts are unchanged.

- **Taste hostile text with a rights-less lane** — SECURITY — value 4 — effort M — risk med — category: agents
  Why: M cells sample the gut and hand only fragments inward. Frontier: 81% worry about security and privacy. Prior art: fencing untrusted text, which still lets the tower read it. Better by: a no-tool child reads issue or CI text and returns a fixed-schema record (kind, file, claim), and the tower never sees raw text. Novelty 3.
  Done when: a planted injection in a fake issue never appears in the tower's context, and a record is still filed.

- **Wall off what can't be cured** — FEATURE — value 4 — effort M — risk low — category: noise
  Why: A granuloma encapsulates what the body can't kill. Evidence: flaky reruns and repeated breakage-ahead false alarms. Prior art: quarantine lists for flaky tests. Better by: any chronic problem (a flaky test, a known-broken module) gets a labelled wall that silences its alarms, with a size gauge that reopens it if it spreads. Novelty 3.
  Done when: a walled flake raises no alert, and a test that makes it fail in a second file reopens the wall.

- **Alert only outside the user's set-point band** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: Homeostasis acts on departure from a set-point, not on events. Assumption: phone or desktop push is wanted but dreaded. Prior art: threshold alerts. Better by: the band is learned per metric from the ledger, and one pocket line is sent only on exit from it. Novelty 3.
  Done when: a quiet week sends zero pushes, and a planted spike sends exactly one line naming the metric.

- **Give new steers a thymic exam** — FEATURE — value 4 — effort S — risk low — category: steers
  Why: Detectors that react to self are deleted before release. A new standing steer can block the user's own normal work. Prior art: none found. Better by: on creation it replays the last 30 days of calls and reports how many of the user's own accepted actions it would have blocked. Novelty 4.
  Done when: a steer written to block a command the user ran 5 times shows "would have blocked 5" before it takes effect.

- **Generate one "how I defend" page from the rules table** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: The ideas so far all add machinery, and the user can't see it. Prior art: hand-written docs. Better by: the page is built from the incident rows, so it can't drift from the code. Novelty 2.
  Done when: adding a rule changes the page, and the sweep fails if the page is stale.

- **Hunt one recurring signature with a self-deleting script (wild)** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: Phages kill one bacterium and nothing else. Assumption: some failures recur monthly with a fixed signature. Prior art: none found. Better by: a tiny single-purpose fixer, bounded by a spend cap, deletes itself after 30 quiet days. Novelty 5.
  Done when: a planted repeating failure is fixed by the hunter, and the hunter file is gone after the quiet window.

- **Sneeze the irritant out of context (wild)** — SECURITY — value 4 — effort M — risk med — category: context
  Why: Sneezing expels the irritant rather than fighting it in place. A blocked hostile fragment otherwise survives in the transcript and in compaction summaries. Prior art: none found. Better by: on a guard block, the offending text is redacted from later summaries and notes. Novelty 4.
  Done when: after a block and a compaction, the hostile string is absent from the summary, and a note says it was removed.

- **Draw the body in `fm doctor` (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: A rough organ map explains the layers (barrier, reflex, memory, thymus) faster than any list. Prior art: none found. Better by: each organ is lit, dim or swollen from real gauges, in 12 lines of ASCII. Novelty 3.
  Done when: killing the guard's liveness canary dims the barrier organ in the output.

Next question: which of these immune ideas does the user ever see work, and which only show up when they fail?
Next question: what would the user delete first if Foreman had to lose a quarter of its learned state tomorrow?
