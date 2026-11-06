# Brainstorm — lens: ecology: keystone species and trophic cascades

- **Run a keystone-removal sweep on the 10,000-moon funnel's own stages** — FEATURE — value 5 — effort M — risk low — category: funnel science
  Why: the funnel is cheap-first (exact dedupe, embedding dedupe, local model, cold read), but no ledger says which stage's unique kills the later stages could not have made. Stages that never kill uniquely are dead weight; stages whose absence floods the top are keystones. Pack evidence: T-2868/2869 built the funnel, with an append-only funnel log that can be replayed.
  Done when: `sampo moons knockout STAGE` replays the funnel log with that stage disabled and prints, per stage, how many candidates reach the cold read that otherwise would not, and the stage with the largest delta is named keystone.

- **Detect mesopredator release between funnel stages** — FEATURE — value 4 — effort S — risk low — category: funnel science
  Why: when a strict late stage (cold read) is relaxed or a strict early stage removed, a mid-stage (embedding dedupe, local scorer) can over-kill or over-pass. The pack shows stage thresholds tuned only singly. Assumption: funnel log stores per-stage verdicts per candidate.
  Done when: a test relaxes one stage in the log replay and the report flags any other stage whose kill rate moved by more than a set margin.

- **Compute a keystone score per verb from simulated extinction** — FEATURE — value 5 — effort M — risk low — category: capability value
  Why: open questions ask "which capability would the user notice first if switched off for a week" and no ledger answers it. Ablate each verb in a lane replay of held-out closed tasks; keystone score is the first-time-pass drop per unit of injected characters.
  Done when: `sampo doctor --keystones` prints a ranked table of verbs with pass-rate delta and character cost, regenerated from a stored replay, and a verb with delta 0 is listed as removable.

- **Trace the trophic cascade of a self-edit through ledgers** — FEATURE — value 4 — effort M — risk med — category: self-edit safety
  Why: the pack's self-edit gates disagree (bench green, Ward exam red) with no record of which is right; a change to one hook propagates to injection size, lane behaviour, exam scores. Record first, second and third order effects per edit.
  Done when: each self-edit commit writes a cascade row listing the metrics that moved beyond noise at one, two and three hops, and `sampo edits cascade ID` prints it.

- **Census the host's apex-predator overlap** — FEATURE — value 4 — effort S — risk low — category: obsolescence
  Why: open question about host features overlapping verbs. Treat each host release as an apex predator entering the web: diff host tool and command lists into a shadow table, mark verbs whose niche is now occupied.
  Done when: on a new Claude Code version, a check lists verbs whose function matches a new host command by description similarity and files a retire-review item for each.

- **Cap unchecked growers (urchin barrens)** — SECURITY — value 4 — effort S — risk low — category: state hygiene
  Why: the 2.4 GB state implies a grower with no predator. Find ledgers with growth rate above their reader count and give each a hard byte cap with a recorded predator (pruner, compactor).
  Done when: `sampo state du --growers` lists every file class with no named predator, and ship fails if one grows more than 10% a week without one.

- **Keep a sentinel-effect sham-off for the Ward** — SECURITY — value 4 — effort M — risk med — category: guard validity
  Why: if the Ward's presence changes agent behaviour (fewer attempts), blocks undercount its value; and its absence is untested. Randomly sham-disable in lane worktrees only, compare attempt rates of guarded commands.
  Done when: a lane run with Ward in audit-only mode logs would-block counts, compared to normal runs, reported in doctor.

- **Audit biomagnification up the summary chain** — SECURITY — value 4 — effort M — risk med — category: injection defence
  Why: untrusted text (repo files, web pages) gets summarised by a local model, then a brief, then an injected line; each hop concentrates it. Tag text with provenance and measure how many hops a planted instruction survives.
  Done when: a planted canary sentence in a fetched file is traced through summaries, and the report shows the hop where it was stripped or not.

- **Profile cascade latency per hook with a trophic budget** — PERFORMANCE — value 4 — effort S — risk low — category: hook speed
  Why: bench_hooks times single hooks; real cost is the chain (SessionStart double injection, Ward, drive). Assign each hook level in the chain and fail ship when the end-to-end chain's p95 exceeds the budget.
  Done when: bench_hooks prints chain p95 per event and the gate fails on a planted 50 ms slowdown.

- **Wild: Reintroduce a dropped capability under a Yellowstone protocol** — FEATURE — value 3 — effort M — risk low — category: retirement
  Why: wild. Retired verbs get re-enabled for one week in a lane at a time to see whether their absence had already created a cascade (more re-asks, more false dones).
  Done when: `sampo retire --reintroduce VERB` runs the lane week and reports re-ask and false-done deltas.

- **Wild: Feed fallen logs to a decomposer lane** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: wild. Dropped tasks, killed moons and failed spikes sit in not-yet.md; a lane mines their blockers for nutrients (a reusable test, a lesson) and files them as cards for small models.
  Done when: one run turns at least 5 dead items into cards or records "no nutrient" with a reason.

- **Wild: Inject a keystone-absence drill into the tower** — SECURITY — value 4 — effort M — risk med — category: resilience
  Why: wild. In a scratch clone, silently remove the top keystone verb and watch which tower rules, gates and sessions fail loudly versus quietly; quiet failures are the real hazard.
  Done when: the drill outputs a list of failures split into loud and silent, and each silent one gets a test.

- **Bound biodiversity of the guard's rule set** — SECURITY — value 3 — effort S — risk low — category: guard validity
  Why: monoculture risk: Ward rules may all catch the same bypass shape. Group rules by the shape they catch and flag shapes covered by one rule only.
  Done when: `sampo ward census` lists shapes with rule counts and flags single-rule shapes.

Next question: Which capability's removal was ever tried in a real session, and what was the measured cascade?
Next question: Does the funnel log record per-stage verdicts per candidate, or only the final fate?
