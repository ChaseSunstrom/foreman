# Brainstorm — lens: invented: the codebase as a living ecosystem

- **Census the ecosystem as a food web** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: ledgers, hooks, skills, verbs and lanes are listed everywhere but never as who-feeds-whom; the pack's "which capability would they notice first" question has no data. assumption: ledger reads/writes are attributable by module.
  Done when: `sampo web` prints a producer→consumer graph from real ledger reads/writes, and flags any verb with zero consumers (a dead trophic level).

- **Name keystone capabilities by removal** — FEATURE — value 5 — effort M — risk low — category: simplicity
  Why: many lean ideas propose weekly mutes and ablations, but none ranks by downstream collapse. Keystone = small footprint, huge effect (Ward, done-gate?). assumption: the long-tier planted-fault scenarios can run with one capability off.
  Done when: a table lists each capability's removal effect on held-out scenarios, and the top three are marked keystone and frozen from lean cuts.

- **Succession stages for new capabilities** — FEATURE — value 4 — effort M — risk med — category: lifecycle
  Why: capabilities arrive all at once at full injection weight. Pioneer (shadow, silent), mid-succession (nudges), climax (injected). Promotion needs measured use; demotion when use fades. Different from "mute a line": it's the default entry path.
  Done when: every new capability starts at the pioneer tier, and `sampo doctor` shows tier and the evidence for each promotion.

- **Mycorrhizal ledger sharing across lanes** — FEATURE — value 4 — effort L — risk med — category: lanes
  Why: lanes pay worktree/state-resolution failures separately and re-learn "tried and failed" facts. assumption: a content-hashed lesson can be shared safely.
  Done when: a lesson one lane records (a failed approach, a worktree quirk) appears in a sibling lane's brief within one tick, tagged with its source lane, and a lane can't write to another's ledger.

- **Quorum-sensed escalation** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: local models are cheap but fail alone; "five-sample jury" appears only as a done-check. Generalise: act only when N independent cheap signals (finder, small model, test, embedding) cross a density threshold, and the density sets the cost tier.
  Done when: `sampo` exposes one quorum function that the funnel, done-gate and moon dedupe call, with a test showing the escalation rate falling as signals agree.

- **Niche-construction receipts** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: Sampo changes the repo to suit later sessions (maps, cards, criteria) but never measures whether the habitat improved. Score each repo's "habitability": time to first correct action for a cold child, before and after.
  Done when: a per-repo habitability number is stored per release, and a cold-child exam shows the number moves when a map is deleted.

- **Trophic cascade tracer for self-edits** — FEATURE — value 4 — effort M — risk med — category: security
  Why: existing ideas gate self-edits by exam, not by second-order effects (cutting one injected line changes nudge rates, which changes block rates). assumption: hook event logs allow before/after rates.
  Done when: each self-edit reports shifts in three downstream rates (nudges, retries after block, false dones) at 7 days, and a shift over threshold opens a revert task.

- **Decomposer lane for dead state** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: the 2.4 GB state is attacked with prune plans, but nothing recycles. Decomposers turn rotted artifacts (old lane worktrees, transcripts) into small nutrients: a lesson, a count, a hash, and then delete.
  Done when: a nightly decomposer retains a digest per expired artifact class and the byte total drops with the digests still answering "what happened in task X".

- **Invasive-species detector for context** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: injected text doubles (double SessionStart) and rename leftovers recur. Flag any text arriving from a second source that wasn't present at baseline, by content hash.
  Done when: a doctor check lists injection fragments with more than one origin or absent from the manifest, and fails on a planted duplicate.

- **Wild: Fire regime — scheduled controlled burns** — FEATURE — value 4 — effort L — risk med — category: lean
  Why: ecosystems that never burn accumulate fuel; Sampo only grows. Quarterly, a lane deletes the most-recent N% of non-keystone prose/rules in a throwaway clone, and only what the exam doesn't miss stays deleted. wild
  Done when: a burn run outputs a deletion diff with exam scores before and after, and applying it requires the user's yes.

- **Wild: Pollinator child** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: ideas move between repos only by the user. A tool-less child carries one pattern (a Ward rule, a lean trick) from a sibling repo's ledger as a "seed", redacted, which the target must grow or reject with a recorded reason. wild
  Done when: a pollination produces a filed brief in a second repo citing the donor, with no donor file contents copied.

- **Wild: Canopy light meter** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the web UI shows bytes and tokens as numbers; an ecosystem reads as light reaching the forest floor. Show how much of the context window the injected "canopy" shades, so the user's actual prompt gets the rest. wild
  Done when: the pane shows one gradient bar for the shaded fraction per turn, matching measured injected characters within 1%.

- **Wild: Seed bank of retired capabilities** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: retirement ideas abound, but ones that die can't return when a weaker model or host regression shows up. Each retired capability keeps a dormant seed (spec, last exam, wake predicate) that germinates when its tripwire fires. wild
  Done when: `sampo seeds` lists dormant capabilities with wake predicates, and a simulated weak-model run re-enables one automatically with a log line.

- **Symbiosis audit with the host** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: Sampo wraps host features; some relationships are mutualism, some parasitism (duplicate task list, duplicate compaction). Classify each verb against host-native equivalents as helps/neutral/costs.
  Done when: each verb carries a classification with a measured cost in tokens or ms, and parasitic ones are listed first.

Next question: Which capabilities have never been removed even once, so no one knows whether they are keystone or dead weight?
Next question: Do ledger writers and readers form cycles that make the food-web graph unstable, so one corrupt ledger poisons many?
