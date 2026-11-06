# Brainstorm — lens: self-modification: finders that learn from which findings were kept, proven or reverted, and improve their own probes, measured and reversible

- **Write a finding-fate ledger keyed by probe and fingerprint** — FEATURE — value 5 — effort M — risk low — category: learning loop
  Why: the pack's exam shows finders found 0 of 108 planted defects, and nothing records which probe produced which kept, proven, dropped or reverted outcome. `fm outcomes` has 30-day survival but no link back to the probe.
  Done when: after a scripted run with 3 findings (one kept, one dropped, one reverted), `fm find ledger` prints one row per finding with probe id, fingerprint and fate, and the numbers match the fixture.

- **Score each probe by proven-fix yield per dollar** — FEATURE — value 5 — effort M — risk low — category: probe metrics
  Why: the pack shows `lens_rates` for brainstorms, but finders have no equivalent. Without a per-probe yield figure no probe edit can be judged.
  Done when: `fm find probes` lists every probe with filed, proven, kept, reverted, dollars and yield, and a probe with zero proofs over N runs is flagged.

- **Store probes as versioned files with one-command revert** — CLEAN — value 4 — effort M — risk low — category: reversibility
  Why: probes live inside fmscout.py and fmeco.py, so any self-edit would be a code change to Foreman. Moving them to data files makes edits small, diffable and undoable.
  Done when: `fm find probe revert NAME` restores the previous version, a test shows the old probe's output returns, and the journal records the revert.

- **Gate every probe edit on a held-out exam with a clean-repo floor** — SECURITY — value 5 — effort M — risk med — category: safety gate
  Why: the steer says weakness-finding uses outside signals only, and `fm exam` already has hidden keys and a holdout third. Reuse that so a self-edit that raises noise, or only wins on the training scenarios, is rejected.
  Done when: a candidate probe edit that adds a false positive on the exam's `none` kind is refused with the score table printed, and one that improves the holdout bugs without new noise is accepted.

- **Mine kept fixes for new probe patterns** — FEATURE — value 4 — effort L — risk med — category: probe generation
  Why: the pack says deterministic finders are blind, while a model finder (plain Claude 3/3) is not. When the model finds and proves a bug, the diff holds a generalisable pattern.
  Done when: given a proven bug-fix diff, `fm find distill` proposes a probe, the probe re-detects the original bug on the pre-fix tree and stays silent on the fixed tree, and it is queued as a candidate, not live.

- **Learn false-positive suppressions from drops and reverts** — FEATURE — value 4 — effort M — risk low — category: noise
  Why: the user's drops are already recorded (the "dropped:" entries); the same signal for findings would stop repeat filings, and a revert is a stronger one.
  Done when: after a user drops a finding, a rescan of the unchanged code does not re-file it. The suppression is keyed by fingerprint and is listed and undoable with `fm find suppress list|rm`.

- **Shadow-run a changed probe before it goes live** — SECURITY — value 4 — effort S — risk low — category: safe rollout
  Why: unasked work in the user's repo is outward-facing, so a new probe version should first report only to the ledger.
  Done when: a probe flagged `shadow` writes findings to the ledger but creates no backlog tasks, and promotion needs N shadow runs with zero reverted outcomes.

- **Cap self-edits with a change budget and an audit trail** — SECURITY — value 4 — effort S — risk low — category: guardrail
  Why: self-modification drifts, and the genesis work already seals gen-0 and diffs privileges. Probe edits need the same discipline.
  Done when: a fourth probe edit in one week is refused, every edit has a ledger event with before/after hashes, and a probe cannot widen its own file-write or network reach.

- **Auto-retire a probe after N noisy filings** — CLEAN — value 3 — effort S — risk low — category: noise
  Why: probe_doctor already queues noise in user projects. A probe whose findings are mostly dropped costs attention and should switch off by itself.
  Done when: a probe whose last N filings were all dropped or unprovable is marked retired, `fm find probes` shows why, and one command revives it.

- **Wild: Plant defects in the user's own repo to grade the finders** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: the exam's planted defects run on fixtures, not on the real stack. Planting bugs in a throwaway worktree copy measures recall where it matters. Assumption: the repo has a runnable test command.
  Done when: `fm find calibrate` plants 5 mutations in a scratch copy, prints how many the probes caught, and leaves the real tree untouched (checked by tree hash).

- **Wild: Breed probes by mutation and kill the weak** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: assumption: with a ledger, a held-out exam and revert, a search over probe variants is cheap to score. Each generation must beat its parent on the holdout or be discarded.
  Done when: one overnight run produces N variants, scores each on the exam's holdout, keeps at most one winner, and the lineage file shows parent, score delta and cost.

- **Wild: Let probes bet on their own findings** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: assumption: each probe states a confidence before filing and is scored on what survives, so over-confident probes lose rank weight. This ties into the value-ranking gap in the mission.
  Done when: a calibration table shows predicted vs actual survival per probe, and rank weights change after a run in the direction the table says.

Next question: Does the exam's `none` kind have enough planted-clean repos to tell a probe edit that adds noise from one that finds real defects?
Next question: Which signal marks a finding as "kept" when the user merges a fix and never says anything: a merge, 30-day survival, or both?
