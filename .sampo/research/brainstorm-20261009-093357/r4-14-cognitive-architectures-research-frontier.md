# Brainstorm — lens: cognitive architectures (research frontier)

- **Hold a sensemaking frame and count the anomalies against it** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: the pack has reframing passes, failure classification and a 3-strikes block, but nothing makes the current frame explicit ("this is a race", "this is config drift") or tracks whether observations still fit it (Klein's data-frame model). Assumption: thrashing on a wrong frame is a common failure.
  Done when: `fm task frame` stores a frame, `fm task anomaly` logs observations that don't fit, and at a set count the drive forces a reframe step before any further edit, shown in the ledger.

- **Localize FIX suspects by reference-frame voting** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm-debugger ranks hypotheses, and "seed FIX plans with ranked suspect lines" is on the list, but as a single ranker. Thousand-Brains-style voting uses independent cheap localizers (stack/trace, co-change history, `fm map` test links, recall of past failures). Each ranks files and the consensus seeds the plan.
  Done when: on 5 replayed past FIX tasks, the consensus top-3 contains the fixed file at least as often as the best single localizer, measured via `fm bench`.

- **Detect action slips against the step's declared intent** — FEATURE — value 4 — effort S — risk low — category: execution
  Why: execute.md has per-step discipline, but a habit-capture slip (running the usual test command or editing the usual file instead of the intended one, per Norman's slip taxonomy) isn't named. The ledger already holds commands and plan steps. Assumption: slips appear in the friction log as "wrong thing verified".
  Done when: a seeded transcript where the step says "run X" and the agent runs the habitual Y produces a flagged slip event, and `fm friction` counts slips by kind.

- **Fit learning curves per task class and act on plateaus** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: `fm friction --every 3` and evolve run on a schedule, and "schedule passes by marginal yield" is listed. Nothing plots first-pass rate against task count per class (the power law of practice), so the system can't tell "still improving" from "stuck, so change the intervention".
  Done when: `fm bench curves` prints per-class first-pass rate over time with a plateau flag, and a plateau opens a recon task naming the class.

- **Build an environment affordance memory** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: lessons and recall are about decisions. Foreman has no procedural model of how this project's tools actually behave (worktree creation is slow, this runner needs `-x`, that gate flakes at 8%). Assumption: the ledger has enough run data to derive it.
  Done when: planning injects an "affordances" note listing at least the 3 most relevant tool behaviors, each cited to ledger events, and an eval shows fewer repeated tool misuse blocks.

- **Verify plan diagrams against the code** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: this uses dual coding as a thinking scaffold. L plans must include a small module/data-flow diagram, and the import graph from `fm map` mechanically checks each edge. An edge the code lacks, or a missing one, is a plan finding.
  Done when: an L plan with a deliberately wrong edge is rejected by `fm task plan` with the offending edge named.

- **Audit Foreman against the Common Model of Cognition** — CLEAN — value 2 — effort S — risk low — category: architecture
  Why: the idea pile has many cognitive faculties (impasses, workspace, activation, FOK) with no map of which couplings exist. Mapping modules to perception, working memory, declarative memory, procedural memory and action shows missing links, like memory that never feeds back into action choice.
  Done when: MASTER.md gains a generated faculty-to-module table, and `fm doctor` flags any faculty with no module or no inbound data flow.

- **Wild: Keep an attention schema** — FEATURE — value 3 — effort M — risk med — category: metacognition
  Why: this follows Graziano's attention schema theory. Each step declares in one line what it is attending to (file, hypothesis, criterion) and a cheap watcher compares that with what the tool calls actually touch. Divergence means attention capture or a rabbit hole. Assumption: the declaration is cheap enough to keep up.
  Done when: a scripted session that wanders to an unrelated file raises an attention-capture note citing the declared and observed targets.

- **Wild: Store mindset bundles as K-lines** — FEATURE — value 3 — effort M — risk med — category: memory
  Why: this follows Minsky's K-lines. When a task goes well, snapshot its mental state (frame, loaded lessons, working-set files, probes used) as a named bundle keyed by task shape. Reactivating it at the next similar task restores the setup, not just facts, and the bench can score whether bundles beat fresh starts. Assumption: recall of lessons alone doesn't carry setup.
  Done when: starting a task matching a stored bundle offers it, and bench shows a measured first-pass or step-count delta versus no bundle.

- **Wild: Ablate priming before committing to a plan** — FEATURE — value 3 — effort S — risk low — category: bias
  Why: the pack lists bias watching and "reread L plans with rationale stripped", but not anchoring by recent context. A tool-less child re-derives the approach from the brief with the last session's context removed, and a differing approach is shown as an anchoring risk.
  Done when: for an L plan, `fm second` reports "same approach" or "approach changes without recent context" with both options listed.

- **Wild: Split wanting from liking in the user's signals** — FEATURE — value 3 — effort M — risk med — category: user model
  Why: the user's words show many asks marked "I like almost all of those", yet the open queue is dozens of captured items. What was asked, what was kept and what was later used or praised are different signals. Tracking them separately stops Foreman over-weighting asks that never get used. Assumption: kept and used are derivable from the ledger and later messages.
  Done when: `fm taste` shows per-category want, keep and use rates, and idea ranking uses the use rate rather than the ask count.

- **Detect pandemonium: cheap demons shout over the event stream** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: Selfridge-style demons, each a tiny rule-based or Haiku watcher on one pattern (repeated read, edit without test, unanswered steer). Instead of one monitor with many rules, the loudest demon above a threshold gets the next nudge, and each demon is scored by whether its nudges changed outcomes. This goes beyond the global-workspace auction because the demons are individually benchable data files.
  Done when: demons are defined as data, at most one nudge per turn is injected, and `fm friction` ranks demons by accepted-nudge rate.

- **Wild: Run a narrator stream the main model can query** — FEATURE — value 2 — effort M — risk med — category: cognition
  Why: a small model writes a running first-person thought stream from the event log, kept cheap and separate from the main context. After compaction or resume the main thread, or the user asking "what are you thinking?", queries it instead of rereading raw ledger lines. Assumption: a derived narrative resumes better than the structured brief alone.
  Done when: after a forced `/compact`, a resume that reads the narrator summary reaches the same next step as the baseline in the chaos-resume test, with fewer tokens read.
