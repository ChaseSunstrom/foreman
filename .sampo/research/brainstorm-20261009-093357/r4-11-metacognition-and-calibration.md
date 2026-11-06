# Brainstorm — lens: metacognition and calibration

- **Expose one trust number for everything Foreman produces** — FEATURE — value 5 — effort M — risk med — category: calibration
  Why: the idea pile has many separate scorecards (per-gate, per-reviewer, per-agent-type, per-lesson, per-panelist, per-epistemic-tag) and nothing joins them. Assumption: they would each need their own reader and format.
  Done when: `fm trust <gate|lesson|reviewer|agent-type|claim-type>` prints an observed hit rate, sample size and interval from the ledger, and `fm ask`, panel weighting and the done-gate read it instead of private numbers.

- **Set every escalation threshold from a cost matrix** — FEATURE — value 4 — effort M — risk med — category: decision thresholds
  Why: the pack has ask-threshold curves, a doubt budget, a "second-opinion yield" and "confidence triggers falsification", each with its own fixed cutoff. Assumption: the costs (false-done, interrupt, extra review) can be expressed in minutes.
  Done when: `fm costs` holds the three costs, and the thresholds for asking, taking a second opinion and falsifying are derived from them. Changing a cost moves the threshold in a test.

- **Forecast in 80% intervals and score coverage** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the open work includes estimates and pace (T-0451) and "calibrate step size", but those are point estimates. A range has a built-in test: 80% intervals should contain the outcome about 80% of the time.
  Done when: briefs record a low–high range for minutes, files touched and steps. At close, `fm friction` shows interval coverage per task type and flags coverage under 60% or over 95%.

- **Score the brief's assumption confidences at close** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: intake writes assumptions with confidence, and `fm task assume` plus T-0052 re-checks exist, but nothing grades the stated confidence. Risks are scored against outcomes; assumptions are not.
  Done when: each assumption is marked held or broken at finish, and a reliability table (stated 90% vs actual) appears in `fm friction`.

- **Scale caution by distance from experience** — FEATURE — value 4 — effort M — risk med — category: novelty awareness
  Why: `fm recall` already runs BM25 over past briefs. The top similarity score is a free "have I seen this kind of task before" signal that nothing uses. Assumption: low similarity correlates with more misses.
  Done when: a task whose best recall match is below a threshold gets a "novel territory" tag, which adds a spike step first and a stricter verify. A bench replay shows whether novel tasks miss more often.

- **Mark beliefs as observed, inferred or carried over from a summary across compaction** — FEATURE — value 4 — effort M — risk low — category: reality monitoring
  Why: Foreman resumes at the exact step after `/compact`, but facts in the summary come back looking as firm as facts just read. Related ideas cover tagging claims and expiring facts, but not demoting a belief that crossed a compaction.
  Done when: after a resume, any load-bearing fact that was only carried over is re-read before an edit or a done claim relies on it. A test plants a stale fact in the summary and the re-read catches it.

- **Audit stopping rules for early and late closure** — FEATURE — value 3 — effort M — risk low — category: process review
  Why: the pack covers when to stop research, brainstorming and retries separately. It has no record of which rule ended each task step (done, block, ask, give up) or whether stopping was later regretted.
  Done when: every finish, block and ask logs the rule that fired. The next-message and rework signals then give a per-rule over-stop and under-stop rate.

- **Break classification ties with evidence before asking** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: intake classifies type and tier, but a close call between FIX and FEATURE, or tier M and L, probably goes to the user or is guessed. Assumption: many ties can be settled by a cheap repo check, such as whether a failing test exists.
  Done when: intake records the top two classes with a margin. A narrow margin runs one read-only probe, and the result and the probe are shown in the brief.

- **Predict the user's next message category every turn** — FEATURE — value 3 — effort M — risk low — category: dense feedback
  Why: calibration labels come only from finished tasks, which are sparse. Every turn gives a label if Foreman predicts accept, revise, bug report or new topic first. Assumption: the prediction costs a few tokens.
  Done when: the ledger holds prediction/outcome pairs, and `fm friction` shows hit rate and the turns where a confident prediction was wrong.

- **Seed calibration on a new repo from its git history** — FEATURE — value 3 — effort M — risk low — category: cold start
  Why: T-0444 (adopt an existing repo) lacks priors, so early confidence on a new project is uncalibrated. Assumption: past commits with tests give cheap labelled outcomes.
  Done when: adoption samples N past commits, predicts from the pre-commit state whether the gates would pass, and stores the hit rate as the project's starting trust prior.

- **Wild: Hunt overconfidence overnight** — FEATURE — value 3 — effort M — risk low — category: red-teaming memory
  Why: wild. `fm night` could pick yesterday's most confident closed claims and ask a cold agent to assume each was wrong and find how, with the diff and evidence as the only input. Confirmed finds become tasks; the rest raise the claim's trust.
  Done when: a seeded wrong-but-confident closure is found in a test, and `fm trust` shows the hunt's confirm rate.

- **Wild: Draw a random blind-spot card** — FEATURE — value 3 — effort S — risk low — category: unknown unknowns
  Why: wild. On roughly one task in N, a cold agent sees only the spec and diff and names the single thing that worries it most, with no checklist. Findings that prove real are tallied by class and promoted to checklist items. The ones that don't are dropped.
  Done when: sampled tasks carry a card, and `fm friction` lists the classes that proved real, with a count.

- **Wild: Keep a "sure and wrong" journal that shapes the prompt** — FEATURE — value 3 — effort S — risk low — category: self-knowledge
  Why: wild. Each confident miss is logged in one line with the domain and the tell. Before planning in the same domain, the plan skill is shown the three most similar entries, which acts as a targeted caution rather than a general rule.
  Done when: planning for a task in a domain with prior entries cites them in the brief, and a bench case shows fewer repeat misses.
