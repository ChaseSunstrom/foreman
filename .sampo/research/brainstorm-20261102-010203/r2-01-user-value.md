# Brainstorm — lens: user value

- **Allow now, adjudicate later** — FEATURE — value 5 — effort L — risk med — category: guard/latency
  Why: users report 15+ approval prompts per session. The innate layer answers in milliseconds and the adaptive layer follows. For reversible calls the hook allows at once, a slow checker re-judges within about a minute, and a bad verdict stops the lane and reverts to a snapshot.
  Done when: a planted harmful-but-reversible call is allowed, then flagged and rolled back within 90s, with zero prompts.
  Prior art: sandboxes with snapshots, but synchronous. Better by: the slow check never blocks the user. Novelty: 4.

- **Detect missing-self** — FEATURE — value 4 — effort M — risk low — category: provenance
  Why: NK cells attack cells that lack the self marker, not cells that look foreign. Every Foreman artifact (commit, edit, lane output) already carries a task or goal trailer, and `fm doctor` flags unstamped changes in tower paths (hand edits, other agents, a harness that skipped hooks).
  Done when: a commit made with no trailer appears in the next session's note, and a stamped one does not.
  Prior art: none found. Better by: catches silence, which pattern guards cannot. Novelty: 4.

- **Post cytokine signals between parallel lanes** — FEATURE — value 4 — effort M — risk low — category: lanes
  Why: lanes in a fan-out repeat each other's traps. A small shared signals file takes one line per hit ("npm test hangs without X"), and PreToolUse in sibling lanes reads it.
  Done when: lane B avoids a trap lane A hit 2 minutes earlier, with no relaunch.
  Prior art: none found in harnesses. Better by: the signal expires with the run, so no lesson pollution. Novelty: 3.

- **Learn commensals during an infancy window** — FEATURE — value 4 — effort S — risk med — category: prompt reduction
  Why: prompts come from friendly-but-unfamiliar commands, such as the user's own scripts, repo `bin/`, and tools in shell history. For the first two weeks Foreman observes and builds a tolerated-shape list, which is shown for one-word revoke, and never covers deny-class verbs.
  Done when: the replay corpus shows no new allow on any deny-class case, and prompts per session fall at least 40% on a fixture history.
  Prior art: prefix allow lists. Better by: shapes are seeded from the user's own environment. Novelty: 3.

- **Boost lessons on a schedule** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: memory wanes. Each lesson not re-triggered in 60 days gets a booster, a tool-less child replaying the original failing scenario with the lesson injected. Lessons that no longer change the outcome are retired.
  Done when: a lesson whose scenario now passes without it is proposed for retirement with the run as proof.
  Prior art: none found. Better by: retirement by test, not by age. Novelty: 3.

- **Re-arm exhausted detectors by checkpoint blockade** — FIX — value 3 — effort S — risk low — category: alarms
  Why: T cells under chronic stimulation go exhausted. Trigger auto-demotion mutes noisy detectors, but nothing brings them back. A muted detector replays on a recent sample and returns at probation level if it is now precise.
  Done when: a demoted trigger with a fixed root cause re-enables itself after a passing replay.
  Prior art: none found. Better by: muting stops being permanent. Novelty: 3.

- **Declare immune-privileged zones** — FEATURE — value 3 — effort S — risk med — category: noise
  Why: some sites, like the eye, suppress reaction because collateral damage costs more than the pathogen. For generated files, lockfiles and scratch dirs, the guard, hints and cold reader stand down, and the status line says so.
  Done when: edits in a declared zone produce zero notes, and `fm doctor` lists the zones.
  Prior art: ignore files. Better by: scoped to Foreman's own reactions. Novelty: 2.

- **Audit original antigenic sin** — FIX — value 3 — effort M — risk low — category: memory
  Why: the first exposure biases later responses. A lesson from incident one can keep firing on variant two and suppress the better fix. Detect lessons recalled before a failure that still recurred, and flag them as imprinted.
  Done when: a fixture lesson recalled before a repeat failure is flagged with both incidents.
  Prior art: none found. Better by: finds lessons that are harmful rather than only stale. Novelty: 4.

- **Measure thymic involution of the replay corpus** — CLEAN — value 3 — effort S — risk low — category: guard quality
  Why: negative selection weakens as the thymus shrinks. The 124 cases date from earlier eras, so report the share of the last 90 days of real commands with a near neighbour in the corpus.
  Done when: `fm replay --drift` prints a coverage percent and names the top 5 unmatched shapes.
  Prior art: none found. Better by: the corpus's age is measured. Novelty: 3.

- **Drain anomalies to a daily lymph node** (wild) — FEATURE — value 3 — effort M — risk low — category: interrupts
  Why: assumption: non-urgent anomalies drain to one digest at a user-chosen hour, with a "swollen" count on the status line, instead of interrupting.
  Done when: a week of fixtures produces one digest and zero mid-session interrupts for non-urgent classes.
  Prior art: notification digests. Better by: urgency is set by damage signals. Novelty: 2.

- **Mine elite controllers from clean sessions** (wild) — FEATURE — value 4 — effort M — risk med — category: learning
  Why: some hosts control a virus without treatment. Instead of learning only from harm, compare the user's longest zero-correction sessions against the worst and surface the habits that differ, such as test-first, small diffs or plan first.
  Done when: `fm doctor` shows three protective habits, each with its sessions and an effect size.
  Prior art: none found. Better by: learns from success and recasts it as nudges. Novelty: 5.

- **Let a lane die by apoptosis** (wild) — FEATURE — value 3 — effort M — risk med — category: containment
  Why: a lane that detects damage to its own working tree or context writes a death note (what, where, last good commit) and exits cleanly. This beats limping on and costing tokens.
  Done when: an injected corruption in a fixture lane ends it within one turn with a note, and the parent files a retry.
  Prior art: none found. Better by: the lane knows when it's broken. Novelty: 4.

- **Run a hygiene challenge week** (wild) — FEATURE — value 3 — effort M — risk med — category: robustness
  Why: sterile environments breed allergies. Once a month, opt-in, a scratch task runs with hints and lessons off to see what the guard alone misses, and feeds new replay cases.
  Done when: a challenge run adds at least one labelled case to the corpus or reports none found.
  Prior art: none found. Better by: finds dependence on Foreman's hand-holding. Novelty: 4.

Next question: which Foreman reactions has the user overridden by hand, and what did they have in common?
Next question: what would the user lose if every immune-style learner were switched off for a month?
