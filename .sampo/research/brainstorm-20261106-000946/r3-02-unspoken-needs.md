# Brainstorm — lens: unspoken needs

- **Be the canary the user isn't: train a "will this published state break?" head on the user's own crash messages** — FEATURE — value 5 — effort M — risk low — category: training signal
  Why: the user is repeatedly the *first* to notice in‑progress‑state breaks — "build.py's moons_html compares r['wild'] >= 4 ... publishes M-59..M-61 with wild null", "The silent-cut scan fails on two cuts", "the site build crashes on an unrated moon". Unspoken: they want to stop being the first line of failure detection; their "fix the crash because…" messages are free labels.
  Done when: a held-out set of past "the tower broke on field X" messages — fed in as partial state — is flagged by the head before the user's message, at ≥50% recall with a named field.

- **Make the latency-fallback a named, traced receipt** — FIX — value 5 — effort S — risk low — category: observability
  Why: answers the leftover question — *which slot abstains/falls back with no ledger trace*. The slot that falls back on **timeout** is invisible because it "just used the rule"; the "measure the fallback" bench can't see it. T-3352 already measures hook ms; the decider's stall path has no equivalent.
  Done when: every model call that hits its time budget emits a ledger line with `cause=timeout`, the slot name, and the rule that won; a `sampo decide --audit` counts them.

- **Carry the user's taste as a portable fingerprint, not a per-repo model** — FEATURE — value 5 — effort L — risk med — category: genericity
  Why: "we will want it to be a generic model ... other things made with sampo." Stated as genericity; unspoken need is *identity continuity* — starting a new project shouldn't mean re-teaching the model what "good" is for *them*.
  Done when: a new canary project cold-starts with the fingerprint and its accept/reject pattern on 10 unseen briefs matches the user's own at ≥70% agreement, with zero project-specific training.

- **Price every decider decision in the user's cost units** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the cost steer — "without burning a fuck ton of money, and quick." Unspoken: they want to *see* the cost-of-being-wrong **per decision** (tokens, wall-clock, a bad push), so "quick and cheap" is visible per call, not a lagging aggregate.
  Done when: each `sampo decide` line carries a `cost` field in tokens + seconds + one "would this have shipped wrongly?" boolean, summing to the morning-card total.

- **Show per-Rune improvement as motion, not a static score** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the request says "how it improves every Rune generation"; unspoken: they don't want to run the bench to *believe* it improved. "Sampo is earning its tokens?" is a point; they need the *delta*.
  Done when: a sparkline of the fixed held-out set across the last N generations is recomputed automatically at each Rune close and is the first line of the generation report.

- **Make unattended decisions self-certifying for the returner** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: "the tower advances itself," "blocked work never sits." Unspoken: return after a week and *trust without auditing*. The need is auditability of the **absence**.
  Done when: a cold, tool-less child can verify any single unattended decision from its receipt in ≤1 step (command + cited evidence + tree-hash), with no repo read beyond the receipt.

- **Suppress settled questions instead of answering them faster** — FEATURE — value 4 — effort S — risk low — category: memory
  Why: the user is annoyed at re-asks ("I meant X, not Y"). Unspoken: they don't want a *faster* answer to a question already decided — they want the question **gone** from the candidate pool.
  Done when: after the user settles a question, the next 5 decider runs on that project surface it zero times as a candidate (negative memory, not a faster lookup).

- **Give the decider self-awareness of its own throughput ceiling** — PERFORMANCE — value 4 — effort M — risk low — category: serving
  Why: "the 10k run judged one 20-moon batch every ~3 min, one at a time, while the endpoint serves 2." Unspoken: "quick" should be *structural* — the decider should know the endpoint's real slots and batch to them, not judge serially by default.
  Done when: the moon-judge throughput on the local endpoint hits ≥ the endpoint's measured concurrent slots, with the batch size chosen from a probe, not hardcoded.

- **Let the decider get quieter when the user does** — wild — FEATURE — value 4 — effort M — risk med — category: unspoken
  Why: answers the leftover "when the user goes quiet for a week, does Sampo know it should be quieter too." Unspoken: they want the decider to read *absence as a signal* and **lower its own volume and ambition** to match — and log that quietness as a reversible decision.
  Done when: after 3 days of no user message, the decider's overnight file-rate and ambition tier drop, and the change appears in the ledger as a named, undoable decision.

- **Let the decider write the morning-after in the user's voice** — wild — FEATURE — value 3 — effort M — risk med — category: delight
  Why: "the tower advances itself" while the user is gone; unspoken: they want to return to something that sounds *managed by someone who knows them*, not a dashboard. Their compression is the tell.
  Done when: the overnight close renders a ≤5-line summary in the user's measured phrasing (learned from their own messages), scored ≥4/5 for "sounds like me" by a cold reader.

- **Give the decider a "I'm guessing on this project" cold-start flag** — wild — FEATURE — value 4 — effort M — risk low — category: genericity
  Why: genericity means the decider will face unseen projects. Unspoken: they'd rather it **flag low confidence on out-of-distribution input and lower its automation**, than decide confidently on a project it hasn't seen.
  Done when: on a project with <20 briefs, the decider emits an `ood` flag that *reduces* its automation tier (more abstain, fewer auto-closes), visible in the status line.

- **Make the decider's identity the user's, exportable as one file** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: "not only one machine," "across sessions." Their rename/migration pain (T-2967, ".foreman/ still named") shows they *hate losing state across a change*. Unspoken: their judgment should be a transferable artifact that survives a Sampo upgrade.
  Done when: `sampo decide export` produces one signed file (weights or distilled preferences) that, restored on a fresh install or new project, reproduces the user's accept/reject pattern at ≥70% with no retraining.

Next question: does the user want the decider to *learn while they're not watching* (train on unattended outcomes) or only while present — i.e., is "training on their behavior" a background process they'd trust running, or one they'd want to explicitly arm each generation?
Next question: which of the user's *own* hand-edits to Sampo-written prose would they *not* want the model to absorb as "taste" — is there a line between "correcting my output" and "teaching me my preferences" that I should ask them to draw before the taste fingerprint is trained?
