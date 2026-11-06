# Brainstorm — lens: learning from outcomes

- **Fuse noisy outcome signals into one label** — FEATURE — value 5 — effort M — risk med — category: outcome labels
  Why: assumption: lessons, scorecards, calibration and bench cases all need "did this task really succeed?", and the pack's signals disagree (gate pass, user silence, a steer, a revert, a reopen). Weak-supervision style: each signal gets a learned reliability, and the output is a probabilistic label with the contributing sources.
  Done when: `fm outcome T-xxxx` prints a label with probability and per-source weights, and a test shows a task with a pass plus a later revert scores below a pass alone.

- **Read the user's follow-up edit as the corrected answer** — FEATURE — value 5 — effort M — risk med — category: user feedback
  Why: the user's own words show cleanup and fixes that "never got done", and their later hand edits are the least ambiguous correction. Mine hunks the user changed within N days in files a done task touched, classify each (bug, style, scope, missing cleanup), and emit candidate lessons or exemplars linked to the task.
  Done when: a fixture where the user edits a done task's file yields a classified candidate lesson citing the task and the hunk.

- **Keep self-changes attributable with a change budget and washout windows** — FEATURE — value 4 — effort M — risk low — category: self-experiment
  Why: friction passes run every 3 tasks and evolve edits instructions, so several changes can land in the same window and nobody can tell which helped. Limit overlapping behaviour changes per area, enforce a washout before the next one, and record the window on each outcome.
  Done when: a second instruction change in the same area during washout is refused or queued, and `fm evolve` reports the attribution window per accepted change.

- **Count the outcomes the ledger never saw** — FIX — value 4 — effort S — risk low — category: survivor bias
  Why: assumption: every metric above is computed from tasks that reached a close. Sessions that were abandoned, compacted away or ended mid-step leave no outcome, so success rates are biased upward. Find open tasks with no events for N days and sessions ending without a close, and count them as censored outcomes.
  Done when: `fm friction` shows a "never closed" count and rate, and success-rate figures state whether censored tasks are included.

- **Adjust lesson-benefit estimates for confounders** — FEATURE — value 4 — effort M — risk low — category: lesson evaluation
  Why: the idea pile has many lesson scorers (recall preceded a clean pass, ablation, confidence). Tier, task type and model mix shift between recalled and unrecalled tasks, so raw comparisons can mislead. Stratify by those fields and report the within-stratum effect with sample size, refusing to credit lessons on thin strata.
  Done when: a synthetic ledger where recall correlates with easy tasks shows near-zero adjusted benefit while the naive figure is positive.

- **Learn the give-up point from attempt curves** — FEATURE — value 4 — effort M — risk low — category: stopping rules
  Why: today it's a flat "3 failed attempts → block". From ledger history, estimate the chance that attempt k+1 succeeds per task type and failure kind, and set the block, split or escalate point where the marginal chance drops below the cost of continuing.
  Done when: `fm task` blocks or escalates at a per-type threshold derived from history, with the estimate shown in the diagnosis, and falls back to 3 with fewer than N samples.

- **Bisect Foreman's own outcome regressions to the commit** — FEATURE — value 4 — effort M — risk med — category: release attribution
  Why: the recent commits include a hook-latency story and releases every few tasks. Run changepoint detection on first-pass rate, steers per task and gate-fail rate aligned to build stamps, then narrow a detected shift to a release or commit range and open a FIX brief.
  Done when: a fixture ledger with an injected drop at version X is flagged with X as the suspect range, and a brief is captured.

- **Estimate pass probability of finished tasks by resampling** — FEATURE — value 3 — effort L — risk med — category: fragile wins
  Why: assumption: a green gate on one run hides tasks that only passed by luck, and their lessons then teach the wrong thing. Replay a sample of closed tasks' execution prompts a few times with bench and mark those with low pass rate as fragile, so their lessons and plan templates are down-weighted.
  Done when: `fm bench --resample N` outputs a pass rate per task, and lessons born from fragile tasks carry a flag that recall shows.

- **Retire eval cases that don't discriminate** — CLEAN — value 3 — effort M — risk low — category: bench quality
  Why: the bench grows from finished tasks and failures, but cases that every variant passes (or fails) consume run time without information. Compute difficulty and discrimination per case from past variant runs and propose retiring or rewriting the dead ones.
  Done when: `fm bench --prune` lists cases with zero variance across at least N variant runs, and removing them leaves variant rankings unchanged on stored data.

- **Wild: Run an island model for instruction variants across projects** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: wild. Each downstream project evolves its own instruction set on its own bench, and winners migrate monthly to other islands for a trial period. This covers the "project-specific vs general" question that the global evolve loop can't.
  Done when: a winning variant on one project is trialled on a second project's bench and either adopted or reported as not transferring.

- **Wild: Post bounties for recurring failure patterns** — FEATURE — value 3 — effort M — risk low — category: overnight swarm
  Why: wild. Clusters of repeating friction and escapes are posted as a bounty with a measurable target (e.g. "cut steers about cleanup by half"). Unattended lanes claim one and are paid only when the metric moves over the next N tasks, not when a fix merges.
  Done when: a bounty closes as paid only after its metric improves, and an unpaid fix is shown as "merged, no effect".

- **Wild: Hold a "did that even matter?" audit of Foreman's own rules** — FEATURE — value 3 — effort M — risk low — category: rule utility
  Why: wild. For each rule or skill, show the tasks in which it fired, what changed in the outcome compared with similar tasks where it didn't, and whether anyone ever complied only because of it. Rules with no measurable effect after a long run get a plain verdict card ("no evidence this does anything") for the user to keep or drop.
  Done when: `fm evolve --report` prints a utility verdict per rule with sample size, and a rule with zero firing tasks is listed as untested rather than useful.
